from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.status import Status
from ..types import UNSET, Unset

T = TypeVar("T", bound="Claim")


@_attrs_define
class Claim:
    """
    Attributes:
        amount_cents (int):
        id (str):
        member_id (str):
        status (Status):
        denial_code (None | str | Unset):
        provider_name (None | str | Unset):
    """

    amount_cents: int
    id: str
    member_id: str
    status: Status
    denial_code: None | str | Unset = UNSET
    provider_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_cents = self.amount_cents

        id = self.id

        member_id = self.member_id

        status = self.status.value

        denial_code: None | str | Unset
        if isinstance(self.denial_code, Unset):
            denial_code = UNSET
        else:
            denial_code = self.denial_code

        provider_name: None | str | Unset
        if isinstance(self.provider_name, Unset):
            provider_name = UNSET
        else:
            provider_name = self.provider_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount_cents": amount_cents,
                "id": id,
                "member_id": member_id,
                "status": status,
            }
        )
        if denial_code is not UNSET:
            field_dict["denial_code"] = denial_code
        if provider_name is not UNSET:
            field_dict["provider_name"] = provider_name

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        amount_cents = d.pop("amount_cents")

        id = d.pop("id")

        member_id = d.pop("member_id")

        status = Status(d.pop("status"))

        def _parse_denial_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        denial_code = _parse_denial_code(d.pop("denial_code", UNSET))

        def _parse_provider_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider_name = _parse_provider_name(d.pop("provider_name", UNSET))

        claim = cls(
            amount_cents=amount_cents,
            id=id,
            member_id=member_id,
            status=status,
            denial_code=denial_code,
            provider_name=provider_name,
        )

        claim.additional_properties = d
        return claim

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
