import { inspectLease } from "./constitution";
import type { CapabilityLease } from "./types";

export function issueLease(input: Omit<CapabilityLease, "id">): CapabilityLease {
  const checked = inspectLease(input);
  if (!checked.ok) throw new Error(checked.reasons.join(" / "));
  return { ...input, id: crypto.randomUUID(), clockAnchor: input.issuedAt };
}

export function leaseState(lease: CapabilityLease, now = new Date(), lastSeenAt?: string): "active" | "expired" | "revoked" | "review-required" {
  if (lease.revokedAt) return "revoked";
  if (lastSeenAt && now.getTime() + 60_000 < new Date(lastSeenAt).getTime()) return "review-required";
  return now.getTime() >= new Date(lease.expiresAt).getTime() ? "expired" : "active";
}

export function renewLease(): never { throw new Error("C-09: Leaseは自動更新できません。新しい明示承認が必要です"); }

