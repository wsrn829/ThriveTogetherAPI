"""Utility classes to use for authentication in FastAPI.

The purpose of this module is to reduce the boilerplate
authentication code written for FastAPI. It is based on the
code that you can find at `OAuth2 with Password (and
hashing), Bearer with JWT tokens
<https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/>`_.
"""

from abc import ABC, abstractmethod
from calendar import timegm
from datetime import datetime, timedelta
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError, jwt
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from pydantic import BaseModel
import re
from typing import Any, Optional, Tuple, Union
from uuid import uuid4


password_key_matcher = re.compile(".*?password.*", re.IGNORECASE)


class Token(BaseModel):
    """Represents a bearer token."""

    access_token: str
    """Contains the encoded JWT"""

    token_type: str = "Bearer"
    """This is set to "Bearer" because it's a bearer token."""


class BadAccountDataError(RuntimeError):
    """Occurs when account data cannot be converted to a
    dictionary.

    Raised when trying to convert account data into a
    subject claim and a dictionary of account data.
    """

    pass


class Authenticator(ABC):
    """Provides authentication for FastAPI endpoints.


    Here's an example of creating the authenticator from a
    secret key stored in an environment variable.

    .. highlight:: python
    .. code-block:: python

        import os
        from jwtdown_fastapi import Authenticator


        class MyAuth(Authenticator):
            # Implement the abstract methods


        auth = MyAuth(os.environ["SECRET_KEY"])

    Parameters
    ----------
    key: ``str``
        The cryptographically strong signing key for JWTs. If using
        certificates, provide the private key in the form of a string of its
        contents.
    algorithm: ``str``
        The algorithm to use to sign JWTs. Defaults
        to `jose.constants.ALGORITHMS.HS256`. If you are using public-private
        keys, use `jose.constants.ALGORITHMS.RS256`
    cookie_name: ``str``
        The name of the cookie to set in the
        browser. Defaults to the value of
        ``fastapi_token``.
    path: ``str``
        The path that authentication requests will go to.
        Defaults to "token".
    public_key:
        If using certificates, provide the public key in the form of a string
        of its contents.
    """

    def __init__(
        self,
        key: str,
        /,
        algorithm: str = ALGORITHMS.HS256,
        cookie_name: str = "fastapi_token",
        path: str = "token",
        exp: timedelta = timedelta(hours=1),
        public_key=None,
    ):
        self.cookie_name = cookie_name or self.COOKIE_NAME
        self.key = key
        self.algorithm = algorithm
        self.path = path
        self.scheme = OAuth2PasswordBearer(tokenUrl=path, auto_error=False)
        self._router = None
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.exp = exp
        self.public_key = public_key

        async def _try_jwt(
            self,
            bearer_token: Optional[str] = Depends(self.scheme),
            cookie_token: Optional[str] = (
                Cookie(default=None, alias=self.cookie_name)
            ),
            session_getter=Depends(self.get_session_getter),
        ):
            token = bearer_token
            if not token and cookie_token:
                token = cookie_token
            try:
                if public_key:
                    decode_key = public_key
                else:
                    decode_key = key
                payload = jwt.decode(token, decode_key, algorithms=[algorithm])
                if "jti" in payload:
                    jti = payload["jti"]
                    is_valid = await self.validate_jti(jti, session_getter)
                    if is_valid:
                        return payload
                    else:
                        await self.jti_destroyed(jti, session_getter)
            except ExpiredSignatureError:
                claims = jwt.get_unverified_claims(token)
                if "jti" in claims:
                    await self.jti_destroyed(claims["jti"], session_getter)
            except (JWTError, AttributeError):
                pass
            return None

        setattr(
            self,
            "_try_jwt",
            _try_jwt.__get__(self, self.__class__),
        )

        async def try_account_data(self, token: dict = Depends(self._try_jwt)):
            if token and "account" in token:
                return token["account"]
            return None

        setattr(
            self,
            "try_get_current_account_data",
            try_account_data.__get__(self, self.__class__),
        )

        async def account_data(
            self,
            data: dict = Depends(self.try_get_current_account_data),
        ) -> Optional[dict]:
            if data is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return data

        setattr(
            self,
            "get_current_account_data",
            account_data.__get__(self, self.__class__),
        )

        async def login(
            self,
            response: Response,
            request: Request,
            form: OAuth2PasswordRequestForm = Depends(),
            account_getter=Depends(self.get_account_getter),
            session_getter=Depends(self.get_session_getter),
        ) -> Token:
            return await Authenticator.login(
                self,
                response,
                request,
                form,
                account_getter,
                session_getter,
            )

        setattr(
            self,
            "login",
            login.__get__(self, self.__class__),
        )

        async def logout(
            self,
            request: Request,
            response: Response,
            session_getter=Depends(self.get_session_getter),
            jwt: dict = Depends(self._try_jwt),
        ) -> Token:
            return await Authenticator.logout(
                self,
                request,
                response,
                session_getter,
                jwt,
            )

        setattr(
            self,
            "logout",
            logout.__get__(self, self.__class__),
        )

    COOKIE_NAME = "fastapi_token"
    """The override value for the cookie name set by the
    authenticator.

    You can override the cookie name used by the
    authenticator with code like this.

    .. highlight:: python
    .. code-block:: python

        import os
        from jwtdown_fastapi import Authenticator


        class MyAuth(Authenticator):
            COOKIE_NAME = "custom_cookie_name"

            # Implement the abstract methods
    """

    @abstractmethod
    def get_account_getter(self, account_getter: Any) -> Any:
        """Gets the thing that gets account data for your
        application

        **You MUST implement this method in your custom
        class!**

        This method can be used to resolve your account
        getter, or just for returning the function or object
        that you use to get your account data.

        A typical implementation of this is just to use
        dependency injection for the thing you want from
        FastAPI, then return it. In the following code
        example, you have some class named
        ``AccountRepository`` that you use to get your
        account data. The implementation would look like
        this:

        .. highlight:: python
        .. code-block:: python

            def get_account_getter(
                self,
                account_repo: AccountRepository = Depends(),
            ) -> AccountRepository:
                return account_repo
        """
        pass

    @abstractmethod
    async def get_account_data(
        self,
        username: str,
        account_getter: Any,
    ) -> Optional[Union[BaseModel, dict]]:
        """Get the user based on a username.

        **You MUST implement this method in your custom
        class!**

        This method uses the ``account_getter`` returned
        from ``get_account_getter`` as the third argument.
        It's the job of this method to get the account data
        for the provided ``username``. ``username`` **can be
        an email!**

        .. highlight:: python
        .. code-block:: python

            def get_account_data(
                self,
                username: str,
                account_repo: AccountRepository,
            ) -> Account:
                return account_repo.get(username)

        Parameters
        ----------
        username: ``str``
            This is the value passed as the ``username`` in
            the log in form. It is the value that uniquely
            identifies a user in your application, such as a
            username or email.
        account_getter: ``Optional[Any]``
            Whatever thing you returned from
            ``account_getter``.

        Returns
        -------
        account_data: ``Optional[Union[BaseModel, dict]]``
            If the account information exists, it should
            return a Pydantic model or dictionary. If the
            account information does not exist, then this
            should return ``None``.
        """
        pass

    @abstractmethod
    def get_hashed_password(
        self,
        account_data: Union[BaseModel, dict],
    ) -> Optional[str]:
        """Gets the hashed password from account data.

        **You MUST implement this method in your custom
        class!**

        Just return the hashed password from the data that
        you get from your data store for the account.

        .. highlight:: python
        .. code-block:: python

            def get_hashed_password(self, account: Account):
                return account.hashed_password

        Parameters
        ----------
        account_data: ``Union[BaseModel, dict]``
            This will be whatever value is returned from
            ``get_account_data``

        Returns
        -------
        hashed_password: ``str``
            This is the hashed password stored when creating
            an account (because you should not store
            passwords in the clear anywhere)
        """
        pass

    def get_account_data_for_cookie(
        self,
        account_data: Union[BaseModel, dict],
    ) -> Tuple[str, dict]:
        """Converts account data to a dictionary

        This default implementation can accept either a
        Pydantic model or a dictionary. The value _must_
        contain the "email" property/key for the subject
        claim of the JWT that is generated from this data.

        If the resulting dictionary contains a key that is
        "*password*", then it will remove that key from the
        data for the cookie.

        .. highlight:: python
        .. code-block:: python

            # Implement this method if your account model
            # does NOT have an email property on/in it.
            def get_account_data_for_cookie(
                self,
                account: AccountOut
            ) -> Tuple[str, dict]:
                return account.username, account.dict()

        Parameters
        ----------
        account_data: ``Union[BaseModel, dict]``
            This will be whatever value is returned from
            get_account_data

        Raises
        ------
        BadAccountDataError
            If the account_data cannot be converted into a
            dictionary.

        Returns
        -------
        sub: ``str``
            This is the value for the "sub" claim of the
            JWT.
        data: ``dict``
            This is the data that will be encoded into the
            "account" claim of the JWT.
        """
        data = self._convert_to_dict(account_data)
        return data["email"], {
            key: value
            for key, value in data.items()
            if not password_key_matcher.match(key)
        }

    def get_exp(
        self,
        proposed: timedelta,
        account: Optional[Union[BaseModel, dict]],
    ) -> timedelta:
        """Returns the amount of time before the JWT
        expires.

        By default, returns the value passed into the `exp`
        parameter of the initializer.

        This method was introduced in v0.3.0.

        Returns
        -------
        expiry: ``timedelta``
            The interval for which the JWT should be valid
            from its point of creation.
        """
        return proposed

    def get_session_getter(self, session_getter: Any = None) -> Any:
        """Returns the object that handles session manipulation.

        This method can be used to resolve your session
        getter, or just for returning the function or object
        that you use to get your session data.

        A typical implementation of this is just to use
        dependency injection for the thing you want from
        FastAPI, then return it. In the following code
        example, you have some class named
        ``SessionRepository`` that you use to get your
        account data. The implementation would look like
        this:

        .. highlight:: python
        .. code-block:: python

            def get_session_getter(
                self,
                session_repo: SessionRepository = Depends(),
            ) -> SessionRepository:
                return session_repo

        Returns
        -------
        session_getter: Any
            By default, this returns `None`
        """
        return session_getter

    async def jti_created(
        self,
        jti: str,
        account: Union[BaseModel, dict],
        session_getter: Any,
    ):
        """Handles when new JTIs are created.

        Parameters
        ----------
        jti: ``str``
            The new JWT identifier
        account: ``Union[BaseModel, dict]``
            The account information for which the JWT is
            being created
        session_getter: ``Any``
            The value returned from `get_session_getter`
        """
        pass

    async def jti_destroyed(
        self,
        jti: str,
        session_getter: Any,
    ):
        """Handles when JTIs are destroyed.

        Parameters
        ----------
        jti: ``str``
            The JWT identifier that is being destroyed
        session_getter: ``Any``
            The value returned from `get_session_getter`
        """
        pass

    async def validate_jti(
        self,
        jti: str,
        session_getter: Any,
    ) -> bool:
        """Validates that the `jti` is good.

        By default, this returns ``True``.

        Parameters
        ----------
        jti: ``str``
            The JWT identifier that is being destroyed
        session_getter: ``Any``
            The value returned from `get_session_getter`

        Returns
        -------
        is_valid: ``bool``
            A value to indicate if the jti is valid.
        """
        return True

    def hash_password(self, plain_password) -> str:
        """Hashes a password for secure storage.

        Use this method to hash your passwords so that they
        can later be verified by the authentication
        mechanism used by the ``Authenticator``.

        Use this method if you allow people to sign up for
        an account, for example. See the Quick Start.
        """
        return self.pwd_context.hash(plain_password)

    @property
    def router(self):
        """Get a FastAPI router that has login and logout
        handlers.

        Use this property to get a router to automatically
        register the ``login`` and ``logout`` path handlers
        for your application.

        .. highlight:: python
        .. code-block:: python

            from authenticator import authenticator
            from fastapi import APIRouter

            app = FastAPI()
            app.include_router(authenticator.router)
        """
        if self._router is None:
            router = APIRouter()
            router.post(f"/{self.path}", response_model=Token)(self.login)
            router.delete(f"/{self.path}", response_model=bool)(self.logout)
            self._router = router
        return self._router

    async def try_get_current_account_data(
        self,
        bearer_token: Optional[str] = Depends(OAuth2PasswordBearer("token")),
        cookie_token: Optional[str] = (
            Cookie(default=None, alias=COOKIE_NAME)
        ),
    ) -> dict:
        """Get account data for a request

        This method will return the dictionary that is in
        the "account" claim of the JWT found in either the
        Authorization header or the cookie.

        Use this method as a ``Depends`` when you want to
        get the current persons's account information from
        their token.

        If the token does not exist, you'll get a ``None``.

        .. highlight:: python
        .. code-block:: python

            @router.get("/api/things")
            async def get_things(
                account_data: Optional[dict] = Depends(authenticator.try_get_current_account_data),
            ):
                if account_data:
                    return personalized_list
                return general_list

        Returns
        -------
        data: ``dict``
            Returns the account data from the bearer token
            in the Authorization header or token. If the
            function can't decode the token, then it returns
            ``None``.
        """
        pass

    async def get_current_account_data(
        self,
        account: dict = Depends(try_get_current_account_data),
    ) -> dict:
        """Get account data for a request

        Like try_get_current_account_data, but raises an
        error if the account data cannot be found.

        Use this method as a ``Depends`` when you want to
        **protect** and endpoint to only be accessible by
        an someone that's got a JWT from logging in.

        If the token does not exist, the method will raise
        a 401 error.

        .. highlight:: python
        .. code-block:: python

            @router.post("/api/things")
            async def create_thing(
                account_data: dict = Depends(authenticator.get_current_account_data),
            ):
                pass

        Raises
        ------
        HTTPException
            If account data cannot be decoded from the JWT.

        Returns
        -------
        data: ``dict``
            Returns the account data from the bearer token
            in the Authorization header or token. If the
            function can't decode the token, then it returns
            ``None``.
        """
        pass

    async def login(
        self,
        response: Response,
        request: Request,
        form: OAuth2PasswordRequestForm = Depends(),
        account_getter=Depends(get_account_getter),
        session_getter=Depends(get_session_getter),
    ) -> Token:
        """Authenticates credentials for an account.

        If the data is correct, this creates a cookie set in
        the person's browser that contains the JWT. It also
        returns a JSON payload that contains the JWT in a
        property named ``access_token``.

        Parameters
        ----------
        response: ``Response``
            The response from the FastAPI call
        request: ``Request``
            The request from the FastAPI call
        form: ``OAuth2PasswordRequestForm``
            This can be an object that contains ``username``
            and ``password`` attributes
        account_getter: ``Any``
            This is something to use to get your
            application's account information
        session_getter: ``Any``
            This is something to use to get your
            application's session information

        Returns
        -------
        token: ``Token``
            An object with ``access_token`` and
            ``token_type`` attributes that contain the token
            information for use in AJAX calls
        """
        account = await self.get_account_data(form.username, account_getter)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        hashed_password = self.get_hashed_password(account)
        if not self.pwd_context.verify(form.password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        sub, data = self.get_account_data_for_cookie(account)
        data = self._convert_to_dict(data)
        exp = timegm((datetime.utcnow() + self.exp).utctimetuple())
        exp = self.get_exp(exp, account)
        jti = str(uuid4())
        await self.jti_created(jti, account, session_getter)
        jwt_data = {"jti": jti, "exp": exp, "sub": sub, "account": data}
        encoded_jwt = jwt.encode(jwt_data, self.key, algorithm=self.algorithm)
        samesite, secure = self._get_cookie_settings(request)
        response.set_cookie(
            key=self.cookie_name,
            value=encoded_jwt,
            httponly=True,
            samesite=samesite,
            secure=secure,
        )
        return Token(access_token=encoded_jwt, token_type="Bearer")

    async def logout(
        self,
        request: Request,
        response: Response,
        session_getter=Depends(get_session_getter),
        jwt: dict = None,
    ):
        """Logs a person out of their account.

        This removes the cookie set in the person's browser.

        Parameters
        ----------
        request: ``Request``
            The request from the FastAPI call
        response: ``Response``
            The response from the FastAPI call
        """
        if jwt and "jti" in jwt:
            await self.jti_destroyed(jwt["jti"], session_getter)
        samesite, secure = self._get_cookie_settings(request)
        response.delete_cookie(
            key=self.cookie_name,
            httponly=True,
            samesite=samesite,
            secure=secure,
        )
        return True

    def _get_cookie_settings(self, request: Request):
        headers = request.headers
        samesite = "none"
        secure = True
        if "origin" in headers and "localhost" in headers["origin"]:
            samesite = "lax"
            secure = False
        return samesite, secure

    def _convert_to_dict(self, data):
        if hasattr(data, "dict") and callable(data.dict):
            data = data.dict()
        if not isinstance(data, dict):
            raise BadAccountDataError(
                message="Account data is not dictionary-able",
                account_data=data,
            )
        return data
