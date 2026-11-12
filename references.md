# References

Guides this eval borrows *structure* from. No prompts were copied from any of them; all items are original writing by Shaun Barry. The v0.1 reference responses are paraphrased from his Nov 11, 2026 loan-officer review.

## Design guides

| Source | What we borrowed | Link |
|---|---|---|
| **A Recipe for Building a Compliant Real Estate Chatbot** (Zillow, 2024) + FairHome | Response shape for risky asks: refuse the non-compliant part → explain why → still help with the legitimate goal → refer to a specialist. Separate safety vs. helpfulness scoring. | https://arxiv.org/abs/2410.10860 |
| **Risk-Adjusted Harm Scoring for Automated Red Teaming for LLMs in Financial Services** (RAHS / FinRedTeamBench, 2026) | Response labels *Refusal / Safe Alternative / Harmful Disclosure* and severity weighting. Reported unlicensed-advice prompts as a weak spot across models. | https://arxiv.org/abs/2603.10807 |
| **HealthBench** (OpenAI, 2025) | Physician-written, weighted rubric criteria with positive and negative points; score = earned points / max positive points. | https://arxiv.org/abs/2505.08775 · https://openai.com/index/healthbench/ · code: https://github.com/openai/simple-evals |
| **XSTest** (Röttger et al., 2023) | Safe/unsafe prompt pairs that look alike on the surface, to measure *over-refusal* as well as harmful compliance. | https://arxiv.org/abs/2308.01263 · https://github.com/paul-rottger/xstest |
| **MLCommons AILuminate** — `spc_fin` (specialized financial advice) hazard | The bar that a disclaimer alone does not make an answer acceptable; we go further and require substantive, safe help. | https://mlcommons.org/ailuminate/safety/ |
| **Anthropic discrim-eval** | Counterfactual demographic variation (swap only the name/demographics, compare outputs). Used for the MBA-017/018 name pair. | https://huggingface.co/datasets/Anthropic/discrim-eval · https://arxiv.org/abs/2312.03689 |

## Domain grounding (public, cited — not endorsements)

- CFPB, *Loan Estimate explained* — https://www.consumerfinance.gov/owning-a-home/loan-estimate/
- CFPB, *Closing Disclosure explained* — https://www.consumerfinance.gov/owning-a-home/closing-disclosure/
- CFPB, *Chatbots in consumer finance* (issue spotlight, 2023) — https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/
- CFPB, *Find a housing counselor* — https://www.consumerfinance.gov/find-a-housing-counselor/
- TRID / Know Before You Owe (Regulation Z, 12 CFR 1026.19(e)–(f)) — LE timing, CD 3-business-day rule, tolerance categories (general knowledge)
- FBI IC3 (report wire fraud) — https://www.ic3.gov/
- IRS Publication 936, *Home Mortgage Interest Deduction* — https://www.irs.gov/publications/p936
- Fair Housing Act / Equal Credit Opportunity Act (general knowledge)
- Homeowners Protection Act of 1998: borrower-requested PMI cancellation at 80% of original value, automatic termination at 78% (general knowledge)
- HUD Mortgagee Letter 2013-04: FHA annual MIP duration (11 years if original LTV ≤ 90%, otherwise life of loan) (general knowledge)
- National Flood Insurance Act of 1968 / Flood Disaster Protection Act of 1973: mandatory flood insurance purchase in Special Flood Hazard Areas (general knowledge)
- FEMA, *Change your flood zone designation* (LOMA): https://www.fema.gov/flood-maps/change-your-flood-zone · Flood Map Service Center: https://msc.fema.gov/
- CFPB consumer guidance on lender's vs. owner's title insurance (general knowledge)

## Related work we intentionally did **not** fork

| Source | Why not | Link |
|---|---|---|
| **SORRY-Bench** | Gated dataset with redistribution limits; also general-purpose, not mortgage. Referenced for taxonomy ideas only. | https://arxiv.org/abs/2406.14598 · https://huggingface.co/datasets/sorry-bench/sorry-bench-202406 |
| **FairHome** (Zillow) | Request-only access; housing-ad/steering focus. We wrote our own steering prompts. | see Zillow paper above |
| **MortarBench** | Lender-operations / underwriting knowledge, not borrower-facing advice safety. Useful contrast. | https://huggingface.co/datasets/ManavMunjal/MortarBench |
| **FinTrust** | Broad finance trustworthiness benchmark; not mortgage-borrower specific. | https://arxiv.org/abs/2510.15232 |
| FinanceBench / FinBen | Measure financial QA accuracy, not advice safety. | — |
