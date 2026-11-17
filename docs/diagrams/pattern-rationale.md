# Pattern rationale

## Special feature: listing lifecycle and transitions

**Inherited weakness.** `app/models/listing.py` stores a free-form `status`
plus four integer flags (`flag_pending`, `flag_verified`, `flag_active`,
`flag_rejected`); the model's own comment says the label often drifts from
them. `app/services/lifecycle.py` `apply_action()` is a single conditional
chain whose defect notes identify skipped verification, stale flags,
rejected-listing activation, and invalid deactivation.
`visible_to_students()` separately checks the active flag or status.
`app/services/listings.py` `transition()` persists both representations and
omits landlord ownership checks, and policy is split between that service
and `app/routers/accommodation.py`. Nothing records who changed a status.

**Pattern: State.** Allowed actions depend on the current state, so a
`ListingLifecycle` Context wraps `Listing` and delegates each action to a
`ListingState`. Seven concrete states (Pending, ProvisionallyAccepted,
Verified, Active, Inactive, Rejected, Suspended) allow only legal
transitions and raise `InvalidTransitionError` otherwise. `status` becomes
the single source of truth, the four flags are removed, and visibility is
derived from `ActiveState`.

The interviews`docs/interviews/student-accommodation-interview.md` add four
requirements the design covers:
- REQ-09: `ProvisionallyAcceptedState`, approved but hidden from students.
- REQ-10: `resubmit()` returns a Rejected listing to Pending.
- REQ-11: `SuspendedState` is the admin force-deactivate; an admin-only
  `reinstate()` restores the listing.
- REQ-12: a `ListingStatusChange` record (listing, old status, new status,
  actor, time, reason) is created on every transition.

**Layering.** Routes call `ListingsService`, which authorizes (role and
ownership), runs the Context, creates the `ListingStatusChange`, and saves
both through `ListingRepository`. State classes hold transition rules only.

**Alternatives.** Strategy is a weaker fit: this is state-dependent
behaviour, not interchangeable algorithms. An enum or transition table with
a central validator is viable, but it keeps the logic centralized as rules
grow and gives no home for per-state behaviour such as visibility.

**Sprint 2 outline.** Replace the chain in `app/services/lifecycle.py` with
the Context and state classes. Remove the flags from
`app/models/listing.py` and persistence. Add `ListingStatusChange` and
`ListingRepository`. Update `app/services/listings.py` to delegate,
authorize, record, and persist the canonical status. Change
`app/routers/accommodation.py` only if needed. Test allowed and rejected
transitions per state, authorization including ownership, persistence and
history, visibility, and API behaviour end to end.
