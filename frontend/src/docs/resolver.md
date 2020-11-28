---
id: resolver
title: Recursive Resolver
---

delivr.dev operates an anycast recursive resolver to decrease cache access times to the authoritative DNS content. 

The resolvers are anycast on `66.248.235.235` / `2a0e:8f00:fe05::235` and have logging disabled and enforce strict DNSSEC validation with the roots.
