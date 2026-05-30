# Data schema v1.5.0

Minimum monthly panel fields for calibration:

| Field | Level | Purpose |
|---|---|---|
| month | time | temporal calibration |
| locality_id | locality | geographic validation |
| practice_id | provider | practice response |
| patient_count | practice/locality | denominator |
| primary_contacts | practice/locality | supply/output |
| booked_to_seen_days | practice/locality | access |
| unmet_need_index | locality | hidden demand |
| ed_presentations | locality | downstream pressure |
| ambulance_conveyances | locality | prehospital pathway |
| public_cost | locality | fiscal output |
| mean_copayment | practice/locality | demand/equity |
| provider_fte_by_scope | practice/locality | workforce/scope |
| acc_claims_and_payments | practice/locality | ACC stabilisation |
| deprivation_ethnicity_rurality_mix | locality | equity validation |
