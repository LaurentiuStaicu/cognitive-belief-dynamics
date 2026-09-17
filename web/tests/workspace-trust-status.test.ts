import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {deriveTrustStatus,type EvidenceSnapshotTrustInput} from '../src/trust-status.ts';

const snapshot=JSON.parse(
 readFileSync(new URL('../../model/evidence_snapshot.json',import.meta.url),'utf8')
) as EvidenceSnapshotTrustInput;

test('online connectivity never upgrades a pinned snapshot to live-verified evidence',()=>{
 const status=deriveTrustStatus(snapshot,{online:true,now:new Date('2026-09-17T12:00:00Z')});
 assert.equal(status.network,'ONLINE');
 assert.equal(status.evidence.mode,'PINNED_BUNDLED_SNAPSHOT');
 assert.equal(status.evidence.freshness,'NOT_LIVE_VERIFIED');
 assert.equal(status.evidence.id,'EVIDENCE.M1.2026-09-16.r1');
 assert.equal(status.evidence.age_days,1);
});

test('offline state does not mutate evidence identity or epistemic freshness',()=>{
 const online=deriveTrustStatus(snapshot,{online:true,now:new Date('2026-09-17T12:00:00Z')});
 const offline=deriveTrustStatus(snapshot,{online:false,now:new Date('2026-09-17T12:00:00Z')});
 assert.equal(offline.network,'OFFLINE');
 assert.deepEqual(offline.evidence,online.evidence);
 assert.equal(offline.offline_guarantee,'NONE_WITHOUT_PRIOR_BROWSER_CACHE');
});

test('policy refuses malformed or future evidence snapshot dates',()=>{
 assert.throws(()=>deriveTrustStatus({...snapshot,as_of:'2026/09/16'},{online:true,now:new Date('2026-09-17T00:00:00Z')}));
 assert.throws(()=>deriveTrustStatus({...snapshot,as_of:'2026-09-18'},{online:true,now:new Date('2026-09-17T00:00:00Z')}));
});
