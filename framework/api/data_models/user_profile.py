from dataclasses import dataclass
from typing import List, Optional, Any, Dict

@dataclass
class UserProfileModel:
    id: int
    cid: int
    email: str
    firstName: str
    lastName: str
    clientType: str
    country: str
    language: str
    registrationDate: str
    isVerified: bool
    emailVerified: bool
    phoneVerified: bool
    isIb: bool
    canRequestIb: bool
    canCreateIbLinks: bool
    ibLinksRestricted: bool
    smsNotificationEnabled: bool
    twoFactorAuthEnabled: bool
    financialPermissions: List[str]
    customFields: List[Any]
    birthDate: Optional[str] = None
    firstDepositDate: Optional[str] = None
    firstDepositId: Optional[int] = None
    lastDepositDate: Optional[str] = None
    lastDepositId: Optional[int] = None
    lastTradedAt: Optional[str] = None
    marketingLinkId: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    referralLinkId: Optional[str] = None
    title: Optional[str] = None
    token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfileModel':

        return cls(
            id=data.get("id"),
            cid=data.get("cid"),
            email=data.get("email"),
            firstName=data.get("firstName"),
            lastName=data.get("lastName"),
            clientType=data.get("clientType"),
            country=data.get("country"),
            language=data.get("language"),
            registrationDate=data.get("registrationDate"),
            isVerified=data.get("isVerified"),
            emailVerified=data.get("emailVerified"),
            phoneVerified=data.get("phoneVerified"),
            isIb=data.get("isIb"),
            canRequestIb=data.get("canRequestIb"),
            canCreateIbLinks=data.get("canCreateIbLinks"),
            ibLinksRestricted=data.get("ibLinksRestricted"),
            smsNotificationEnabled=data.get("smsNotificationEnabled"),
            twoFactorAuthEnabled=data.get("twoFactorAuthEnabled"),
            financialPermissions=data.get("financialPermissions", []),
            customFields=data.get("customFields", []),
            birthDate=data.get("birthDate"),
            firstDepositDate=data.get("firstDepositDate"),
            firstDepositId=data.get("firstDepositId"),
            lastDepositDate=data.get("lastDepositDate"),
            lastDepositId=data.get("lastDepositId"),
            lastTradedAt=data.get("lastTradedAt"),
            marketingLinkId=data.get("marketingLinkId"),
            password=data.get("password"),
            phone=data.get("phone"),
            referralLinkId=data.get("referralLinkId"),
            title=data.get("title"),
            token=data.get("token")
        )