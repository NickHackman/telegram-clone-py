#!/usr/bin/env python3
from enum import Enum


class StatusCode(Enum):
    """
    HTTP Status Codes in the form of (code: int, reason: str)

    To unpack them (code, reason) = StatusCode.OK.value
    """

    def is_error(self) -> bool:
        """
        Check to see if a StatusCode is an Error

        Returns
        -------

        bool
             Whether or not the StatusCode is an error
        """
        (code, reason) = self.value
        return 400 <= code <= 599

    def is_client_error(self) -> bool:
        """
        Check to see if a StatusCode is a Client Error

        Returns
        -------

        bool
             Whether or not the StatusCode is a client error
        """
        (code, reason) = self.value
        return 400 <= code <= 499

    def is_server_error(self) -> bool:
        """
        Check to see if a StatusCode is a Server Error

        Returns
        -------

        bool
             Whether or not the StatusCode is a server error
        """
        (code, reason) = self.value
        return 500 <= code <= 599

    def __str__(self) -> str:
        """
        String of StatusCode

        "{code}: {reason}"

        Returns
        -------

        str
             StatusCode in string form
        """
        code: int = self.value
        return f"{code}: {self.name}"

    # Information
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    PROCESSING = 102

    # success
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226

    # redirection
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308

    # client error
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    REQUEST_ENTITY_TOO_LARGE = 413
    REQUEST_URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451

    # server errors
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511
