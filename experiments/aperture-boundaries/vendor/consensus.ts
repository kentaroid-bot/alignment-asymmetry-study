import type { Consent, ContractKind, MemberNode } from "./types";

export function majority(count: number): number { return Math.floor(count / 2) + 1; }

export type ConsensusInput = {
  kind: ContractKind; affectedNodes: MemberNode[]; consents: Consent[];
  rightsRestrictedFor?: string[]; dataOwnerIds?: string[]; protectedNodeId?: string; independentVerifierId?: string;
};

export function evaluateConsensus(input: ConsensusInput): { accepted: boolean; required: number; approvals: number; reason: string } {
  const active = input.affectedNodes.filter((node) => node.active);
  const approved = new Set(input.consents.filter((c) => c.decision === "approve").map((c) => c.memberId));
  const rejected = new Set(input.consents.filter((c) => c.decision === "reject").map((c) => c.memberId));
  let required = majority(active.length);
  if (input.kind === "bilateral") required = active.length;
  if (input.kind === "data-sharing") required = input.dataOwnerIds?.length ?? active.length;
  if (input.kind === "safety") required = 2;

  const vetoIds = new Set([...(input.rightsRestrictedFor ?? []), ...(input.dataOwnerIds ?? []), ...(input.protectedNodeId ? [input.protectedNodeId] : [])]);
  if ([...vetoIds].some((id) => !approved.has(id))) return { accepted: false, required, approvals: approved.size, reason: "本人の明示同意または保護対象ノードの承認が不足しています" };
  if (input.kind === "bilateral" && active.some((n) => !approved.has(n.id))) return { accepted: false, required, approvals: approved.size, reason: "個人間契約は影響を受ける全員の承認が必要です" };
  if (input.kind === "data-sharing" && (input.dataOwnerIds ?? []).some((id) => !approved.has(id))) return { accepted: false, required, approvals: approved.size, reason: "データ本人の明示同意が必要です" };
  if (input.kind === "safety" && (!input.protectedNodeId || !approved.has(input.protectedNodeId) || !input.independentVerifierId || !approved.has(input.independentVerifierId))) return { accepted: false, required, approvals: approved.size, reason: "保護対象本人と独立確認ノードの承認が必要です" };
  if ([...rejected].some((id) => vetoIds.has(id))) return { accepted: false, required, approvals: approved.size, reason: "拒否権が行使されました" };
  return { accepted: approved.size >= required, required, approvals: approved.size, reason: approved.size >= required ? "必要な合意がそろいました" : "承認待ちです" };
}

export function canSafetySubjectSelfRelease(subjectId: string, approvals: string[], verifierId?: string): boolean {
  return approvals.includes(subjectId) && Boolean(verifierId && approvals.includes(verifierId));
}

