from __future__ import annotations
from abc import ABC, abstractmethod


class ManuscriptStateError(Exception):
    pass


class ManuscriptState(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def can_edit(self) -> bool:
        pass

    @abstractmethod
    def submit(self) -> str:
        pass


class DraftState(ManuscriptState):
    @property
    def name(self) -> str:
        return "DRAFT"

    def can_edit(self) -> bool:
        return True

    def submit(self) -> str:
        return "SUBMITTED"


class SubmittedState(ManuscriptState):
    @property
    def name(self) -> str:
        return "SUBMITTED"

    def can_edit(self) -> bool:
        return False

    def submit(self) -> str:
        raise ManuscriptStateError("Le manuscrit est déjà soumis.")


class InReviewState(ManuscriptState):
    @property
    def name(self) -> str:
        return "IN_REVIEW"

    def can_edit(self) -> bool:
        return False

    def submit(self) -> str:
        raise ManuscriptStateError("Le manuscrit est déjà en relecture.")


class AcceptedState(ManuscriptState):
    @property
    def name(self) -> str:
        return "ACCEPTED"

    def can_edit(self) -> bool:
        return False

    def submit(self) -> str:
        raise ManuscriptStateError("Le manuscrit est déjà accepté.")


class RejectedState(ManuscriptState):
    @property
    def name(self) -> str:
        return "REJECTED"

    def can_edit(self) -> bool:
        return False

    def submit(self) -> str:
        raise ManuscriptStateError("Le manuscrit a été rejeté.")


def get_state(status: str) -> ManuscriptState:
    mapping = {
        "DRAFT": DraftState(),
        "SUBMITTED": SubmittedState(),
        "IN_REVIEW": InReviewState(),
        "ACCEPTED": AcceptedState(),
        "REJECTED": RejectedState(),
    }

    state = mapping.get(status)
    if state is None:
        raise ManuscriptStateError(f"Statut inconnu: {status}")
    return state
