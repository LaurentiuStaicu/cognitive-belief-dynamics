from cognitive_epistemic_model.editorial import (
    EditorialPolicy,
    editorial_select,
    reference_information_pool,
    update_issue_appraisal,
)


def test_val_m1_001_selective_factual_emphasis_changes_sample_and_appraisal():
    pool = reference_information_pool()

    neutral = editorial_select(pool, EditorialPolicy(emphasis=0.0, budget=3))
    negative = editorial_select(pool, EditorialPolicy(emphasis=-1.0, budget=3))

    assert all(unit.compatible_with_facts for unit in neutral.units)
    assert all(unit.compatible_with_facts for unit in negative.units)
    assert negative.balance < neutral.balance

    neutral_appraisal = update_issue_appraisal(
        prior_appraisal=0.0,
        observed_balance=neutral.balance,
    )
    negative_appraisal = update_issue_appraisal(
        prior_appraisal=0.0,
        observed_balance=negative.balance,
    )

    assert negative_appraisal < neutral_appraisal


def test_val_m1_n01_without_editorial_selection_condition_difference_disappears():
    pool = reference_information_pool()

    neutral_null = editorial_select(
        pool,
        EditorialPolicy(emphasis=0.0, budget=3),
        enabled=False,
    )
    negative_null = editorial_select(
        pool,
        EditorialPolicy(emphasis=-1.0, budget=3),
        enabled=False,
    )

    assert neutral_null.units == negative_null.units == pool
    assert neutral_null.balance == negative_null.balance == 0.0
    assert update_issue_appraisal(
        prior_appraisal=0.0,
        observed_balance=neutral_null.balance,
    ) == update_issue_appraisal(
        prior_appraisal=0.0,
        observed_balance=negative_null.balance,
    )


def test_negative_valence_is_not_treated_as_falsehood():
    pool = reference_information_pool()
    negative = editorial_select(pool, EditorialPolicy(emphasis=-1.0, budget=3))
    assert negative.balance < 0.0
    assert all(unit.compatible_with_facts for unit in negative.units)
