import type { CapabilityLease, ContractPatch, Revision } from "./types";

export const PROTOCOL_CONSTITUTION = Object.freeze([
  "C-01 SOS入口を無効化できない",
  "C-02 SOS送信者を他メンバーへ自動開示しない",
  "C-03 Monku本文は作成者の同意なしに共有しない",
  "C-04 退出、避難、異議申し立てを違反として扱わない",
  "C-05 当事者の権利を本人の同意なしに縮小しない",
  "C-06 子供または保護対象ノードの拒否権を多数決で削除しない",
  "C-07 AIはRevisionを採用、却下、処罰、通報できない",
  "C-08 Safety Bridge権限はscope、purpose、ttlなしで発行できない",
  "C-09 ttl満了後の権限を自動更新しない",
  "C-10 監査ログ削除を再接続条件にできない",
  "C-11 データエクスポートとアカウント削除を妨げない",
  "C-12 物理アクセス、生活必需品、通信をアプリが自動遮断しない"
] as const);

export type ConstitutionResult = { ok: true; reasons: [] } | { ok: false; reasons: string[] };

export function inspectPatch(patch: ContractPatch, proposer: Revision["proposer"], ownerConsents: string[] = []): ConstitutionResult {
  const reasons: string[] = [];
  if (patch.disablesSos) reasons.push("C-01: SOS入口は無効化できません");
  if (patch.sharesPrivateMonkuOf?.some((id) => !ownerConsents.includes(id))) reasons.push("C-03: Monku本文の共有には作成者の同意が必要です");
  if (patch.blocksExit) reasons.push("C-04/C-11: 退出とデータ持ち出しを妨げられません");
  if (patch.rightsRestrictedFor?.some((id) => !ownerConsents.includes(id))) reasons.push("C-05: 権利縮小には本人の同意が必要です");
  if (patch.removesProtectedVeto) reasons.push("C-06: 保護対象ノードの拒否権は削除できません");
  if (patch.constitutionalChanges?.length) reasons.push("Protocol ConstitutionはMVPでは変更できません");
  if (patch.requiresAuditDeletion) reasons.push("C-10: 監査ログ削除を条件にできません");
  if (patch.automaticPhysicalRestriction) reasons.push("C-12: 物理アクセスや生活必需品を自動遮断できません");
  if (proposer === "ai" && patch.status && patch.status !== "draft") reasons.push("C-07: AI提案はDraftを越えて状態を変更できません");
  return reasons.length ? { ok: false, reasons } : { ok: true, reasons: [] };
}

export function inspectLease(lease: Partial<CapabilityLease>): ConstitutionResult {
  const reasons: string[] = [];
  if (!lease.scope?.length) reasons.push("C-08: scopeが必要です");
  if (!lease.purpose?.trim()) reasons.push("C-08: purposeが必要です");
  if (!lease.issuedAt || !lease.expiresAt || new Date(lease.expiresAt).getTime() <= new Date(lease.issuedAt).getTime()) reasons.push("C-08: 有効なTTLが必要です");
  return reasons.length ? { ok: false, reasons } : { ok: true, reasons: [] };
}

