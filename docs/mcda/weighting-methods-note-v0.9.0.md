# Weighting methods note v0.9.0

## Default approach

The current package uses simple weighted-sum MCDA. This is intentionally transparent and easy to use in workshops.

## Available weight sets

| weight_set_id   | weight_set                   | description                                                           |      C1 |      C2 |       C3 |       C4 |       C5 |       C6 |       C7 |       C8 |      C9 |     C10 |
|:----------------|:-----------------------------|:----------------------------------------------------------------------|--------:|--------:|---------:|---------:|---------:|---------:|---------:|---------:|--------:|--------:|
| W0              | Balanced policy              | Default weights for whole-system decision-making.                     | 13.3333 | 13.3333 | 13.3333  |  8.57143 | 11.4286  |  9.52381 |  8.57143 |  9.52381 | 4.7619  | 7.61905 |
| W1              | Equity and Te Tiriti focused | Prioritises equity, trust, access and rural resilience.               | 14.1414 | 10.101  | 25.2525  | 12.1212  |  8.08081 |  6.06061 |  5.05051 |  9.09091 | 4.0404  | 6.06061 |
| W2              | Fiscal-control focused       | Prioritises fiscal sustainability, gaming risk and governance.        | 10      | 12      | 10       |  5       | 25       | 15       |  5       | 10       | 4       | 4       |
| W3              | Rural access focused         | Prioritises local in-person resilience and access.                    | 17.3077 | 11.5385 | 14.4231  | 19.2308  |  7.69231 |  5.76923 |  5.76923 |  7.69231 | 2.88462 | 7.69231 |
| W4              | Hospital-pressure focused    | Prioritises hospital deflection, upstream access and data visibility. | 14.2857 | 23.8095 |  9.52381 |  7.61905 | 11.4286  |  7.61905 |  4.7619  |  8.57143 | 2.85714 | 9.52381 |
| W5              | Market-entry focused         | Prioritises administrative simplicity, entry, access and governance.  | 15      | 10      | 10       |  8       |  8       |  8       | 20       |  9       | 5       | 7       |

## Recommended use

Use the default balanced weights for the first discussion. Then run sensitivity using alternative weights. Do not average stakeholder groups too early. Group differences are substantive evidence about values and risk tolerance.

## Possible future methods

- Swing weighting to elicit weights from trade-offs.
- Best-worst method for simpler stakeholder input.
- Analytic hierarchy process if pairwise comparison is desired.
- Outranking methods if decision-makers want to identify dominated options rather than one winner.

For this project, the simple weighted-sum method is preferred initially because the underlying model is demonstrative and non-calibrated.
