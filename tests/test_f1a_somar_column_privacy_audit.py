from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1a_somar_column_privacy_audit.json"
SCHEMA = ROOT / "schemas" / "f1a_somar_column_privacy_audit.schema.json"
DOC = ROOT / "docs" / "F1A_SOMAR_COLUMN_PRIVACY_AUDIT.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_column_privacy_audit_matches_schema() -> None:
    audit = load(CONTRACT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(audit)


def test_audit_preserves_recovery_tested_boundary() -> None:
    audit = load(CONTRACT)
    assert audit["current_stage"] == "RECOVERY_TESTED"
    assert audit["empirical_promotion_authorized"] is False
    assert audit["numerical_calculation_authorized"] is False
    assert audit["next_gate"]["automatic_calculation_allowed"] is False


def test_exact_columns_remain_unverified() -> None:
    audit = load(CONTRACT)
    q = audit["candidate_component_quantity"]
    assert q["status"] == "CONCEPTUALLY_CONDITIONAL_ON_SHARED_INVENTORY_NUMERICALLY_BLOCKED"
    assert q["paper_analysis_shared_inventory_supported"] is True
    assert q["current_release_shared_inventory_verified"] is False
    assert q["interpretable_as_release_view_rate_without_shared_inventory_proof"] is False
    assert q["exact_numerator_column_verified"] is False
    assert q["exact_denominator_column_verified"] is False
    assert "exact_potential_audience_column_name" in audit["unresolved_blockers"]
    assert "exact_exposed_audience_column_name" in audit["unresolved_blockers"]


def test_no_cross_product_privacy_inference() -> None:
    p = load(CONTRACT)["privacy_state"]
    assert p["aggregate_only"] is True
    assert p["url_share_threshold_gt_100_us_users"] is True
    assert p["additional_release_controls_verified"] is False
    assert p["differential_privacy_assumed_from_other_meta_products"] is False


def test_legacy_artifacts_are_identified_but_not_claimed_inspected() -> None:
    d = load(CONTRACT)["verified_legacy_documentation"]
    assert d["data_dictionary_filename"] == "data_dictionary_political_segregation_paper.xlsx"
    assert d["variable_descriptions_filename"] == "variables_political_segregation_paper.csv"
    assert d["exact_dictionary_contents_inspected"] is False
    assert d["current_release_version_linkage_verified"] is False
    assert d["legacy_manifest_source"]["somar_record"] == "34"
    assert d["legacy_manifest_source"]["evidence_role"] == "LEGACY_RETRIEVAL_PROVENANCE_ONLY"
    assert d["legacy_manifest_source"]["current_release_linkage_established"] is False
    locators = d["legacy_artifact_locators"]
    assert locators["data_dictionary"]["file_uuid"] == "ae0be9b4-8297-4231-9e76-08df5ac120af"
    assert locators["data_dictionary"]["size_bytes"] == 44149
    assert locators["variable_descriptions"]["file_uuid"] == "086fb4cb-8cb6-4934-90c1-2a737d3dad62"
    assert locators["project_codebook"]["file_uuid"] == "2d333798-bd6c-478b-81b8-dc51812d96c2"
    assert locators["glossary"]["file_uuid"] == "b6da33f6-8850-44cb-84f4-50565cc2e17d"
    assert "current_release_documentation_file_identity_for_300450_and_300470" in load(CONTRACT)["unresolved_blockers"]


def test_doc_keeps_negative_gate_explicit() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "NUMERICAL_PAIRING_NOT_AUTHORIZED" in text
    assert "No field name is inferred" in text
    assert "F1a remains **RECOVERY_TESTED**" in text


def test_current_somar_public_documentation_route_is_explicit() -> None:
    audit = load(CONTRACT)
    policy = audit["current_public_documentation_access_policy"]
    assert policy["restricted_use_codebooks_and_documentation_publicly_downloadable"] is True
    assert policy["controlled_download_documentation_publicly_downloadable"] is True
    assert policy["vde_documentation_publicly_downloadable"] is True
    assert policy["restricted_data_application_is_not_a_prerequisite_to_read_public_documentation"] is True
    assert policy["exact_dictionary_rows_exposed_by_current_automated_web_surface"] is False
    assert policy["dataset_search_matches_documentation_file_contents"] is False
    assert policy["catalog_search_failure_is_not_evidence_of_documentation_absence"] is True
    assert policy["source"] == "https://www.icpsr.umich.edu/sites/somar/research-lifecycle"
    assert policy["corroborating_icpsr_source"] == "https://www.icpsr.umich.edu/sites/icpsr/about/history"
    assert policy["icpsr_documentation_files_public_by_definition"] is True

    for study in ("potential_exposure", "exposure", "engagement"):
        assert audit["verified_studies"][study]["released_updated_on"] == "2026-04-01"

    route = audit["next_gate"]["preferred_retrieval_path"]
    assert route[:2] == [
        "PUBLIC_DATA_AND_DOCUMENTATION_DOWNLOAD_ICPSR_300450",
        "PUBLIC_DATA_AND_DOCUMENTATION_DOWNLOAD_ICPSR_300470",
    ]

    text = DOC.read_text(encoding="utf-8")
    assert "publicly downloadable" in text
    assert "tooling/retrieval limitation" in text
    assert "does **not** establish" in text


def test_legacy_record_and_doi_identifiers_are_traceability_only() -> None:
    audit = load(CONTRACT)

    potential = audit["verified_studies"]["potential_exposure"]
    assert potential["legacy_somar_record"] == "36"
    assert potential["legacy_public_doi"] == "10.3886/snmc-n870"

    engagement = audit["verified_studies"]["engagement"]
    assert engagement["legacy_somar_record"] == "34"
    assert engagement["legacy_public_doi"] == "10.3886/n3r7-br77"

    exposure = audit["verified_studies"]["exposure"]
    assert exposure["legacy_somar_record"] == "32"
    assert exposure["legacy_public_doi"] is None
    assert exposure["legacy_public_doi_verified"] is False
    assert exposure["legacy_public_doi_status"] == "AMBIGUOUS_DUPLICATE_V3_CODEBOOK_TRANSCRIPTION"
    assert exposure["legacy_public_doi_candidates"] == [
        "10.3886/rnr8-jj22",
        "10.3886/rnr8-ij22",
    ]
    assert exposure["legacy_public_doi_candidate_sources"] == [
        "https://socialmediaarchive.org/record/68/files/US2020_FB%26IG_Elections_External_Codebook_v3.pdf",
        "https://socialmediaarchive.org/record/70/files/US2020_FB%26IG_Elections_External_Codebook_v3.pdf",
    ]
    assert exposure["legacy_public_doi_duplicate_v3_divergence_verified"] is True
    assert exposure["legacy_public_doi_registry_adjudicated"] is False
    assert exposure["legacy_public_doi_record_level_metadata_adjudicated"] is False
    assert exposure["legacy_public_doi_evidence_pattern"] == "V2_AND_ONE_V3_SUPPORT_JJ22_SECOND_V3_SUPPORTS_IJ22"
    assert exposure["legacy_public_doi_v2_jj22_verified"] is True
    assert exposure["legacy_public_doi_v3_jj22_verified"] is True
    assert exposure["legacy_public_doi_v3_ij22_verified"] is True
    assert exposure["legacy_public_doi_jj22_has_cross_version_support"] is True
    assert exposure["legacy_public_doi_cross_version_support_sufficient_for_canonical_selection"] is False
    assert "legacy_exposure_doi_transcription_conflict" in audit["unresolved_blockers"]

    legacy = audit["verified_legacy_documentation"]
    assert legacy["current_release_version_linkage_verified"] is False
    assert any("legacy Exposure record 32 is stable" in x for x in audit["interpretation_boundary"])


def test_icpsr_collection_versioning_keeps_legacy_linkage_unverified() -> None:
    audit = load(CONTRACT)
    policy = audit["icpsr_collection_versioning_policy"]
    assert policy["data_or_documentation_file_change_triggers_new_collection_version"] is True
    assert policy["addition_or_withdrawal_of_data_or_documentation_triggers_new_collection_version"] is True
    assert policy["individual_files_versioned_separately"] is False
    assert policy["collection_level_version_statement_required"] is True
    assert policy["legacy_filename_record_doi_or_title_match_sufficient_for_current_version_linkage"] is False
    assert policy["source"] == "https://www.icpsr.umich.edu/sites/icpsr/posts/shared/access-earlier-version"

    legacy = audit["verified_legacy_documentation"]
    assert legacy["current_release_version_linkage_verified"] is False
    assert any("ICPSR versions the collection as a whole" in x for x in audit["interpretation_boundary"])


def test_current_collection_identity_is_asymmetric_and_non_inferred() -> None:
    audit = load(CONTRACT)
    current = audit["current_collection_identity"]

    p = current["potential_exposure"]
    assert p["icpsr"] == "300450"
    assert p["study_page"] == "https://www.icpsr.umich.edu/sites/somar/view/studies/300450"
    assert p["doi"] == "10.3886/ICPSR300450.V2"
    assert p["version"] == "V2"
    assert p["doi_and_version_verified"] is True

    e = current["exposure"]
    assert e["icpsr"] == "300470"
    assert e["study_page"] == "https://www.icpsr.umich.edu/sites/somar/view/studies/300470"
    assert e["doi"] is None
    assert e["version"] is None
    assert e["doi_and_version_verified"] is False
    assert "not exposed" in e["reason_unverified"]
    assert any("not inferred by analogy" in x for x in audit["interpretation_boundary"])


def test_current_metadata_routes_replace_retired_oai_path() -> None:
    audit = load(CONTRACT)
    route = audit["metadata_export_access_state"]
    assert route["batch_metadata_api_current"] is True
    assert route["batch_metadata_api_requires_credentials"] is True
    assert route["individual_study_export_metadata_current"] is True
    assert route["individual_study_export_formats"] == ["Dublin Core", "DDI-Codebook"]
    assert route["legacy_oai_status"] == "RETIRED"
    assert route["legacy_oai_study_base_url"] == "https://pcms.icpsr.umich.edu/pcms/api/1.0/oai/studies"
    assert route["sufficient_for_variable_dictionary_gate"] is False
    assert route["current_300470_metadata_payload_obtained"] is False
    assert route["current_api_credentials_requirement_reconfirmed_on"] == "2026-09-25"
    assert route["retired_oai_continuity_statement"] == "AVAILABLE_UNTIL_AT_LEAST_2026-08"
    assert route["retired_oai_continuity_guarantee_covers_audit_date"] is False
    assert route["retired_oai_target_300470_payload_recovered_through_audited_surface"] is False
    assert route["retired_oai_reliable_current_fallback"] is False
    assert route["retired_oai_getrecord_target_studies_attempted"] == ["300450", "300470"]
    assert route["retired_oai_getrecord_formats_attempted"] == ["oai_dc", "oai_ddi25"]
    assert route["retired_oai_getrecord_payloads_obtained"] is False
    assert route["retired_oai_getrecord_failure_interpretable_as_record_absence"] is False
    assert route["retired_ddi_bulk_archive_url"] == "https://www.icpsr.umich.edu/files/ICPSR/or/metadata/xml/abstracts.tar.gz"
    assert route["retired_ddi_bulk_archive_officially_linked"] is True
    assert route["retired_ddi_bulk_archive_description"] == "MONTHLY_COMPRESSED_8000_PLUS_DDI_XML_STUDY_RECORDS"
    assert route["retired_ddi_bulk_archive_fetch_attempted_on"] == "2026-09-25"
    assert route["retired_ddi_bulk_archive_payload_inspected"] is False
    assert route["retired_ddi_bulk_archive_fetch_result"] == "BINARY_CONTENT_DISCOVERED_TOOLING_CANNOT_RENDER_OR_DOWNLOAD"
    assert route["retired_ddi_bulk_archive_noninspection_interpretable_as_absence"] is False
    assert route["retired_ddi_bulk_archive_potential_role"] == "STUDY_METADATA_IDENTITY_AND_PROVENANCE_ONLY"
    assert route["retired_ddi_bulk_archive_sufficient_for_variable_dictionary_gate"] is False
    assert any("older OAI-PMH/DDI endpoint is retired" in x for x in audit["interpretation_boundary"])


def test_icpsr_indexed_documentation_discovery_is_fallback_only() -> None:
    audit = load(CONTRACT)
    d = audit["icpsr_indexed_documentation_discovery"]

    assert d["ssvd_searches_variable_name_label_question_text_and_value_labels"] is True
    assert d["ssvd_all_catalog_studies_have_variable_level_documentation"] is False
    assert d["main_data_search_indexes_all_available_study_documentation"] is True
    assert d["main_data_search_includes_variable_descriptions"] is True
    assert d["thematic_collection_search_equivalent_to_main_icpsr_search"] is False
    assert d["individual_study_variable_search_documented"] is True
    assert d["current_300450_or_300470_variable_level_result_obtained"] is False
    assert d["intended_role"] == "PUBLIC_INDEX_DISCOVERY_FALLBACK"
    assert d["sufficient_for_variable_dictionary_gate"] is False

    assert any("SOMAR thematic/catalog search limitation" in x for x in audit["interpretation_boundary"])
    assert any("SSVD can expose variable-level names" in x for x in audit["interpretation_boundary"])

    text = DOC.read_text(encoding="utf-8")
    assert "ICPSR indexed-documentation discovery fallback" in text
    assert "does not pass the variable-dictionary gate" in text


def test_variable_search_endpoint_failure_is_not_negative_evidence() -> None:
    audit = load(CONTRACT)
    d = audit["icpsr_indexed_documentation_discovery"]

    assert d["public_global_variable_search_endpoint"] == "https://www.icpsr.umich.edu/web/ICPSR/search/variables"
    assert d["current_automated_surface_can_execute_parameterized_variable_queries"] is False
    assert d["parameterized_query_failure_interpretable_as_variable_absence"] is False
    assert d["variables_tab_absence_redirects_to_codebook"] is True
    assert d["variables_tab_absence_guidance_source"].endswith("/how-to-find-a-dataset")


def test_legacy_exposure_url_disclosure_scope_conflict_stays_blocking() -> None:
    audit = load(CONTRACT)
    conflict = audit["legacy_exposure_url_disclosure_scope_conflict"]

    assert conflict["source_role"] == "LEGACY_CODEBOOK_ONLY"
    assert conflict["url_level_context_verified"] is True
    assert conflict["conflicting_disclosure_scope"] == "DOMAIN"
    assert conflict["exact_url_level_audience_aggregation_semantics_verified"] is False
    assert conflict["v2_technical_section_source"].endswith("US2020_FB%26IG_Elections_External_Codebook_v2.pdf")
    assert conflict["url_data_categorization_verified"] is True
    assert conflict["aggregation_subsection_declared_level"] == "URL"
    assert conflict["disclosures_subsection_declared_level"] == "DOMAIN"
    assert conflict["structural_section_conflict_verified"] is True
    assert conflict["conflict_scope"] == ["DISCLOSURES"]
    assert conflict["v2_url_level_aggregation_and_domain_level_disclosure_coexist"] is True
    assert conflict["v3_overview_url_specific_aggregation_verified"] is True
    assert conflict["v3_overview_resolves_v2_overview_scope_ambiguity"] is True
    assert conflict["v3_disclosures_subsection_text_recovered"] is False
    assert conflict["v3_disclosure_scope_verified"] is False
    assert conflict["v3_exact_url_level_audience_aggregation_semantics_verified"] is False
    assert conflict["v3_scope_resolution_status"] == "OVERVIEW_URL_CONSISTENT_DISCLOSURE_SUBSECTION_UNINSPECTED"
    assert conflict["status"] == "V2_URL_AGGREGATION_DOMAIN_DISCLOSURE_CONFLICT_V3_DISCLOSURE_UNINSPECTED"
    assert "legacy_exposure_url_disclosure_scope_wording_conflict" in audit["unresolved_blockers"]
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Legacy Exposure URL disclosure scope conflict" in text
    assert "must not be imported" in text
    assert "A later indexed **v3** codebook narrows this conflict" in text


def test_metadata_schema_confirms_doi_expected_but_not_recovered() -> None:
    audit = load(CONTRACT)
    route = audit["metadata_export_access_state"]

    assert route["current_metadata_schema_source"] == "https://icpsr.github.io/metadata/icpsr_metadata_schema/"
    assert route["current_metadata_schema_last_updated"] == "2026-09-22"
    assert route["legacy_metadata_schema_source"] == "https://icpsr.github.io/metadata/icpsr_legacy_schema/"
    assert route["current_schema_doi_required"] is True
    assert route["legacy_schema_doi_required"] is True
    assert route["current_schema_doi_includes_study_number_and_version"] is True
    assert route["current_schema_substantive_major_change_creates_new_version_specific_doi"] is True
    assert route["current_300470_doi_expected_in_canonical_metadata"] is True
    assert route["current_300470_doi_value_obtained"] is False
    assert route["current_300470_version_inference_from_schema_or_neighbor_study_allowed"] is False
    assert route["current_metadata_style_guide_source"] == "https://icpsr.github.io/metadata/icpsr_style_guide/"
    assert route["current_300470_unversioned_doi_reference"] == "https://doi.org/10.3886/ICPSR300470"
    assert route["current_300470_unversioned_doi_reference_rule_verified"] is True
    assert route["current_300470_unversioned_doi_target_resolution_verified"] is False
    assert route["unversioned_doi_reference_sufficient_for_version_specific_identity"] is False

    exposure = audit["current_collection_identity"]["exposure"]
    assert exposure["doi"] is None
    assert exposure["version"] is None
    assert exposure["doi_and_version_verified"] is False
    assert "concrete DOI/version value" in exposure["reason_unverified"]
    assert any("metadata-retrieval failure" in x for x in audit["interpretation_boundary"])
    assert any("no version suffix is inferred" in x for x in audit["interpretation_boundary"])


def test_manual_browser_codebook_route_is_explicit_and_noninferential() -> None:
    audit = load(CONTRACT)
    route = audit["manual_browser_documentation_retrieval"]

    assert route["icpsr_navigation_source"].endswith("/adopt-a-dataset-classroom-edition")
    assert route["restricted_data_codebook_source"].endswith("/how-do-i-know")
    assert route["somar_public_documentation_source"].endswith("/research-lifecycle")
    assert route["documented_navigation_path"] == [
        "OPEN_CURRENT_ICPSR_STUDY_PAGE",
        "OPEN_DATA_AND_DOCUMENTATION_TAB",
        "LOCATE_RELEVANT_DATASET",
        "OPEN_DOWNLOAD_DROPDOWN_NEXT_TO_DATASET",
        "SELECT_CODEBOOK_OR_ICPSR_CODEBOOK",
        "INSPECT_VARIABLE_DOCUMENTATION",
        "RECORD_CURRENT_COLLECTION_VERSION_AND_DOCUMENTATION_FILE_IDENTITY",
    ]
    assert route["codebook_access_precedes_restricted_data_application"] is True
    assert route["restricted_data_application_required_to_read_public_codebook"] is False
    assert route["manual_route_execution_status"] == "DOCUMENTED_NOT_EXECUTED"
    assert route["manual_route_executed_in_this_audit"] is False
    assert route["manual_route_next_required_step"] is True
    assert route["verified_on"] == "2026-09-25"
    assert route["target_specific_indexed_documentation_search_retried_on"] == "2026-09-25"
    assert route["target_specific_indexed_documentation_search_studies"] == ["300450", "300470"]
    assert route["target_specific_indexed_documentation_search_terms"] == ["Data & Documentation", "Codebook", "ICPSR Codebook", "data dictionary", "download"]
    assert route["target_specific_indexed_documentation_file_url_obtained"] is False
    assert route["target_specific_indexed_dataset_file_listing_obtained"] is False
    assert route["target_specific_indexed_search_reexposed_catalog_only"] is True
    assert route["direct_study_pages_shell_only_through_audited_surface"] is True
    assert route["automated_indexed_route_exhausted_for_available_audited_tooling"] is True
    assert route["automated_indexed_route_exhaustion_equivalent_to_manual_route_exhaustion"] is False
    assert route["manual_interactive_route_required"] is True
    assert route["manual_route_send_precondition_satisfied"] is False
    assert route["intended_role"] == "NONINFERENTIAL_MANUAL_RETRIEVAL_FALLBACK"
    assert route["automated_surface_current_300450_dataset_file_listing_obtained"] is False
    assert route["automated_surface_current_300470_dataset_file_listing_obtained"] is False
    assert route["current_300450_dictionary_contents_obtained"] is False
    assert route["current_300470_dictionary_contents_obtained"] is False
    assert route["sufficient_for_variable_dictionary_gate"] is False

    preferred = audit["next_gate"]["preferred_retrieval_path"]
    assert "MANUAL_ICPSR_DATA_AND_DOCUMENTATION_CODEBOOK_RETRIEVAL" in preferred
    assert audit["numerical_calculation_authorized"] is False
    assert any("noninferential manual route" in x for x in audit["interpretation_boundary"])

    text = DOC.read_text(encoding="utf-8")
    assert "Manual browser retrieval path" in text
    assert "Codebook" in text
    assert "does **not** pass the variable-dictionary gate" in text


def test_icpsr_public_data_facet_does_not_override_restriction_state() -> None:
    audit = load(CONTRACT)
    state = audit["icpsr_search_access_interpretation"]

    assert state["search_surface_public_data_facet_present_for_somar_results"] is True
    assert state["current_300450_catalog_states_restricted_and_application_required"] is True
    assert state["current_300470_catalog_states_restricted_and_application_required"] is True
    assert state["icpsr_tracks_data_availability_and_restriction_type_separately"] is True
    assert state["general_public_availability_can_coexist_with_use_restrictions"] is True
    assert state["public_data_facet_sufficient_to_infer_unrestricted_analytic_data_files"] is False
    assert state["public_data_facet_sufficient_to_pass_documentation_gate"] is False
    assert state["metadata_api_source"] == "https://icpsr.github.io/metadata/icpsr_metadata_api/"

    assert any("Public Data availability facet" in x for x in audit["interpretation_boundary"])
    assert any("availability and restriction type" in x for x in audit["interpretation_boundary"])
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Public Data facet versus restricted-use status" in text
    assert "must not be interpreted as evidence that the restricted analytic data files are openly downloadable" in text


def test_300470_versioned_route_probe_does_not_promote_candidate_to_verified_version() -> None:
    audit = load(CONTRACT)
    probe = audit["current_300470_versioned_route_probe"]

    assert probe["candidate_route"].endswith("/300470/versions/V1.0")
    assert probe["control_counterexample_source"].endswith("/300464/versions/V1.0")
    assert probe["candidate_route_http_surface_responds"] is True
    assert any(x.endswith("/300470/versions/V2.0") for x in probe["negative_control_routes_rejected"])
    assert any(x.endswith("/300470/versions/V99.0") for x in probe["negative_control_routes_rejected"])
    assert probe["candidate_route_exposes_study_title_in_automated_html"] is False
    assert probe["candidate_route_exposes_version_label_in_automated_html"] is False
    assert probe["candidate_route_exposes_doi_in_automated_html"] is False
    assert probe["candidate_route_exposes_study_identifier_in_automated_html"] is False
    assert probe["current_300470_version_verified_from_route"] is False
    assert probe["current_300470_version_value"] is None

    exposure = audit["current_collection_identity"]["exposure"]
    assert exposure["version"] is None
    assert exposure["doi"] is None
    assert exposure["doi_and_version_verified"] is False
    assert audit["numerical_calculation_authorized"] is False

    assert probe["route_version_can_differ_from_current_collection_version"] is True
    assert probe["candidate_route_informative_about_current_version"] is False
    assert probe["candidate_route_priority_for_current_version_inference"] == "NONE"
    assert probe["control_counterexample_route_version"] == "V1.0"
    assert probe["control_counterexample_current_version_exposed"] == "V2.0"
    assert any("route responsiveness is not evidence" in x for x in audit["interpretation_boundary"])
    text = DOC.read_text(encoding="utf-8")
    assert "300470 versioned-route probe" in text
    assert "does **not** verify V1.0" in text


def test_legacy_potential_exposure_url_scope_conflict_stays_blocking() -> None:
    audit = load(CONTRACT)
    conflict = audit["legacy_potential_exposure_url_aggregation_scope_conflict"]

    assert conflict["source_role"] == "LEGACY_CODEBOOK_ONLY"
    assert conflict["table"] == "potential_exposure_facebook_posts_with_civic_news_urls"
    assert conflict["url_level_context_verified"] is True
    assert conflict["conflicting_aggregation_scope"] == "DOMAIN"
    assert conflict["exact_url_level_potential_audience_aggregation_semantics_verified"] is False
    assert conflict["status"] == "DOCUMENTATION_SCOPE_CONFLICT_UNRESOLVED"
    assert conflict["conflict_observed_in_multiple_legacy_codebooks"] is True
    assert conflict["corroborating_source"].endswith("US2020_FB%26IG_Elections_External_Codebook.pdf")
    assert conflict["v3_scope_resolution_verified"] is True
    assert conflict["v3_scope_resolution_status"] == "CONFLICT_PERSISTS_IN_INDEXED_V3_CODEBOOK"
    assert conflict["conflict_observed_in_legacy_versions"] == ["DRAFT", "V2", "V3"]
    assert conflict["v3_source"].endswith("US2020_FB%26IG_Elections_External_Codebook_v3.pdf")
    assert conflict["url_data_categorization_verified"] is True
    assert conflict["aggregation_subsection_declared_level"] == "DOMAIN"
    assert conflict["disclosures_subsection_declared_level"] == "DOMAIN"
    assert conflict["structural_section_conflict_verified"] is True
    assert conflict["conflict_scope"] == ["OVERVIEW", "AGGREGATION", "DISCLOSURES"]
    assert "legacy_potential_exposure_url_aggregation_scope_wording_conflict" in audit["unresolved_blockers"]
    assert audit["candidate_component_quantity"]["exact_denominator_column_verified"] is False
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Legacy Potential Exposure URL aggregation scope conflict" in text
    assert "must not be imported as the URL-level denominator aggregation rule" in text


def test_legacy_current_identity_concordance_is_not_an_explicit_crosswalk() -> None:
    audit = load(CONTRACT)
    c = audit["legacy_current_identity_concordance"]

    assert c["status"] == "MULTI_FIELD_IDENTITY_CONCORDANCE_EXPLICIT_MIGRATION_CROSSWALK_UNVERIFIED"
    assert c["explicit_record_to_icpsr_crosswalk_found"] is False
    assert c["explicit_record_specific_redirect_found"] is False
    assert c["title_only_match_sufficient_for_mapping"] is False
    assert c["concordance_establishes_current_release_linkage"] is False
    assert c["role"] == "PROVENANCE_DISCOVERY_ONLY_NOT_RELEASE_LINKAGE"

    expected = {
        "potential_exposure": ("36", "300450"),
        "exposure": ("32", "300470"),
        "engagement": ("34", "300475"),
    }
    for key, (legacy_record, current_icpsr) in expected.items():
        m = c["mappings"][key]
        assert m["legacy_somar_record"] == legacy_record
        assert m["current_icpsr"] == current_icpsr
        assert m["exact_title_match"] is True
        assert m["url_level_match"] is True
        assert m["study_period_match"] is True
        assert m["broad_population_match"] is True
        assert m["semantic_role_match"] is True
        assert m["explicit_migration_mapping_verified"] is False

    assert "explicit_legacy_record_to_current_icpsr_migration_crosswalk" in audit["unresolved_blockers"]
    assert audit["numerical_calculation_authorized"] is False
    assert any("concord with current ICPSR" in x for x in audit["interpretation_boundary"])
    assert any("migration crosswalk" in x for x in audit["interpretation_boundary"])

    text = DOC.read_text(encoding="utf-8")
    assert "Legacy-to-current identity concordance" in text
    assert "does **not** establish an explicit migration crosswalk" in text


def test_replication_code_access_is_separate_from_public_documentation_gate() -> None:
    audit = load(CONTRACT)
    r = audit["replication_code_access_boundary"]

    assert r["science_states_deidentified_data_and_analysis_code_archived_in_somar_for_eligible_research"] is True
    assert r["current_author_page_uses_apply_for_replication_code_and_data"] is True
    assert r["icpsr_release_states_us2020_data_access_via_vde_application"] is True
    assert r["public_documentation_access_is_separate_from_replication_code_access"] is True
    assert r["public_codebook_or_dictionary_remains_preferred_gate_source"] is True
    assert r["public_replication_code_repository_verified"] is False
    assert r["absence_of_public_code_repository_interpretable_as_missing_documentation"] is False
    assert r["controlled_replication_code_required_before_public_documentation_attempts"] is False
    assert r["controlled_replication_code_can_substitute_for_current_release_dictionary_without_version_linkage"] is False
    assert r["intended_role"] == "PROCEDURAL_ACCESS_BOUNDARY"
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Replication-code access is a separate gate" in text
    assert "does not make restricted code access a prerequisite" in text


def test_external_source_id_is_not_a_public_crosswalk_route() -> None:
    audit = load(CONTRACT)
    r = audit["migration_crosswalk_metadata_route"]

    assert r["legacy_external_source_id_field_exists"] is True
    assert r["legacy_external_source_id_internal_only"] is True
    assert r["legacy_external_source_id_publicly_displayed"] is False
    assert r["current_schema_external_source_id_field_present"] is False
    assert r["current_schema_version_history_field_present"] is True
    assert r["current_schema_version_note_is_provenance_field"] is True
    assert r["public_export_expected_to_expose_legacy_external_source_id"] is False
    assert r["version_history_or_notes_are_valid_public_provenance_targets"] is True
    assert r["current_300450_version_history_payload_obtained"] is False
    assert r["current_300470_version_history_payload_obtained"] is False
    assert r["explicit_migration_crosswalk_resolved"] is False
    assert r["sufficient_for_current_release_linkage"] is False
    assert r["intended_role"] == "PUBLIC_PROVENANCE_ROUTE_QUALIFICATION"

    assert any("External Source ID field cannot be treated as a public" in x for x in audit["interpretation_boundary"])
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Migration-crosswalk metadata route" in text
    assert "not publicly displayed" in text


def test_current_300450_dictionary_availability_is_verified_but_contents_remain_uninspected() -> None:
    audit = load(CONTRACT)
    d = audit["current_target_documentation_availability"]
    p = d["potential_exposure"]
    e = d["exposure"]

    assert p["icpsr"] == "300450"
    assert p["current_doi"] == "10.3886/ICPSR300450.V2"
    assert p["current_version"] == "V2"
    assert p["current_doi_and_version_verified"] is True
    assert p["current_page_explicitly_offers_data_dictionary_download"] is True
    assert p["current_data_dictionary_availability_verified"] is True
    assert p["current_data_dictionary_file_identity_obtained"] is False
    assert p["current_data_dictionary_contents_obtained"] is False
    assert p["exact_physical_columns_verified"] is False

    assert e["icpsr"] == "300470"
    assert e["current_doi"] is None
    assert e["current_version"] is None
    assert e["current_doi_and_version_verified"] is False
    assert e["target_specific_current_page_data_dictionary_offer_recovered"] is False
    assert e["current_data_dictionary_availability_target_specifically_verified"] is False
    assert e["current_data_dictionary_file_identity_obtained"] is False
    assert e["current_data_dictionary_contents_obtained"] is False
    assert e["absence_of_target_specific_index_hit_interpretable_as_documentation_absence"] is False

    assert d["sufficient_for_variable_dictionary_gate"] is False
    assert audit["candidate_component_quantity"]["exact_denominator_column_verified"] is False
    assert audit["candidate_component_quantity"]["exact_numerator_column_verified"] is False
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Current target documentation availability" in text
    assert "300450" in text
    assert "availability is verified" in text
    assert "300470" in text


def test_published_replication_code_doi_is_locator_not_dictionary_proof() -> None:
    audit = load(CONTRACT)
    r = audit["replication_code_access_boundary"]

    assert r["published_replication_code_title"] == "Meta Platforms, Inc. Replication Code for U.S. 2020 Facebook and Instagram Election Study"
    assert r["published_replication_code_doi"] == "10.3886/spb3-g558"
    assert r["published_replication_code_distributor"] == "Inter-university Consortium for Political and Social Research"
    assert r["published_replication_code_distribution_date"] == "2023-07-27"
    assert r["published_replication_code_archived_at_somar_icpsr"] is True
    assert r["published_replication_code_vde_access_as_cited"] is True
    assert r["published_replication_code_scope_to_science_ade7138_verified"] is False
    assert r["published_replication_code_contents_inspected_in_this_audit"] is False
    assert r["published_replication_code_sufficient_for_exact_300450_300470_column_gate"] is False
    assert audit["numerical_calculation_authorized"] is False
    assert any("10.3886/spb3-g558" in x for x in audit["interpretation_boundary"])

    text = DOC.read_text(encoding="utf-8")
    assert "10.3886/spb3-g558" in text
    assert "does not by itself identify the physical columns" in text


def test_science_paper_table_mapping_supports_selection_not_current_release_linkage() -> None:
    audit = load(CONTRACT)
    m = audit["science_paper_table_mapping"]

    assert m["paper_doi"] == "10.1126/science.ade7138"
    assert m["codebook_appendix_explicitly_maps_paper_to_dataset_family"] is True
    assert m["target_dataset_titles_explicitly_associated"] == [
        "Potential Exposure to Facebook Posts with Civic News URLs",
        "Exposure to Facebook Posts with Civic News URLs",
        "Engagement with Facebook Posts with Civic News URLs",
    ]
    assert m["supports_candidate_potential_exposure_to_exposure_pairing_design"] is True
    assert m["supports_current_2026_release_file_linkage"] is False
    assert m["supports_exact_physical_column_identity"] is False
    assert m["supports_release_specific_privacy_semantics"] is False
    assert m["numerical_pairing_authorized"] is False
    assert m["paper_states_each_url_has_potential_exposed_engaged_audience_measures"] is True
    assert m["paper_same_url_conceptual_pairing_supported"] is True
    assert m["paper_same_url_pairing_scope"] == "ANALYSIS_CONCEPT_NOT_RELEASE_ROW_IDENTITY"
    assert m["current_release_same_url_row_presence_verified"] is False
    assert m["current_release_absent_row_semantics_verified"] is False
    assert m["current_release_suppression_filter_symmetry_verified"] is False
    assert m["current_release_url_key_equivalence_verified"] is False
    assert m["current_release_rowwise_pairing_authorized"] is False
    assert m["role"] == "PAPER_SAME_URL_CONCEPTUAL_PAIRING_NOT_CURRENT_RELEASE_ROWWISE_LINKAGE"
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Science paper-to-dataset mapping" in text
    assert "does not establish current 2026 release linkage" in text
    assert "same-URL conceptual pairing" in text


def test_author_replication_link_is_collection_level_not_article_specific() -> None:
    audit = load(CONTRACT)
    r = audit["replication_code_access_boundary"]

    assert r["additional_author_research_source"] == "https://jenpan.com/"
    assert r["science_replication_link_target"] == "https://socialmediaarchive.org/search?c=US2020&cc=US2020&ln=en"
    assert r["science_replication_link_is_us2020_collection_level"] is True
    assert r["science_replication_link_article_specific_package_resolved"] is False
    assert r["same_collection_replication_link_reused_for_multiple_us2020_publications"] is True
    assert r["published_replication_code_scope_to_science_ade7138_verified"] is False
    assert audit["numerical_calculation_authorized"] is False


def test_science_vn_is_analysis_weight_not_r_view_release_field() -> None:
    audit = load(CONTRACT)
    w = audit["science_analysis_weighting_boundary"]

    assert w["analysis_quantity_symbol"] == "v_n"
    assert w["paper_description"] == "total number of unique views for domain or URL n"
    assert w["paper_role"] == "SEGREGATION_INDEX_VISIT_WEIGHT"
    assert w["same_as_release_content_views_field_verified"] is False
    assert w["same_as_release_exposed_audience_users_field_verified"] is False
    assert w["same_as_release_audience_field_verified"] is False
    assert w["exact_release_field_mapping_verified"] is False
    assert w["usable_as_r_view_numerator"] is False
    assert w["usable_as_r_view_denominator"] is False
    assert w["usable_to_resolve_current_300470_column_identity"] is False
    assert w["dictionary_mapping_required"] is True
    assert "science_vn_analysis_weight_to_release_field_mapping" in audit["unresolved_blockers"]
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Science analysis-weighting boundary" in text
    assert "`v_n` cannot be used as the numerator or denominator of `r_view`" in text


def test_somar_help_is_documentation_locator_escalation_before_vde() -> None:
    audit = load(CONTRACT)
    s = audit["official_documentation_support_escalation"]

    assert s["support_contact"] == "somar-help@umich.edu"
    assert s["restricted_data_application_required_before_support_request"] is False
    assert s["vde_application_required_before_support_request"] is False
    assert s["support_request_is_evidence_of_documentation_contents"] is False
    assert s["support_request_authorizes_numerical_pairing"] is False
    assert s["intended_role"] == "DOCUMENTATION_LOCATOR_ESCALATION_BEFORE_RESTRICTED_DATA_ACCESS"
    assert s["trigger_condition"] == "MANUAL_PUBLIC_DATA_AND_DOCUMENTATION_ROUTE_EXECUTED_WITHOUT_TARGET_DOCUMENT_RECOVERY"
    assert s["manual_public_documentation_route_must_be_attempted_first"] is True
    assert s["send_precondition_satisfied"] is False

    route = audit["next_gate"]["preferred_retrieval_path"]
    support = route.index("SOMAR_HELP_PUBLIC_DOCUMENTATION_LOCATOR_REQUEST")
    vde = route.index("APPROVED_SOMAR_VDE_RELEASE_DOCUMENTATION_ONLY_IF_PUBLIC_DOCUMENTATION_IS_INSUFFICIENT")
    assert support < vde
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Official SOMAR Help escalation" in text
    assert "before any VDE application" in text


def test_author_replication_navigation_targets_do_not_establish_article_specific_package() -> None:
    audit = load(CONTRACT)
    r = audit["replication_navigation_locators"]

    assert r["hunt_allcott_legacy_target"] == "https://socialmediaarchive.org/record/43?ln=en"
    assert r["hunt_allcott_target_reused_for_multiple_us2020_publications"] is True
    assert r["hunt_allcott_legacy_target_redirects_to_current_somar_home"] is True
    assert r["hunt_allcott_record_43_metadata_payload_recovered"] is False
    assert r["hunt_allcott_record_43_file_listing_recovered"] is False
    assert r["hunt_allcott_record_43_identity_as_published_replication_code_doi_verified"] is False

    assert r["jennifer_pan_target"] == "https://socialmediaarchive.org/search?c=US2020&cc=US2020&ln=en"
    assert r["jennifer_pan_target_is_collection_level"] is True
    assert r["jennifer_pan_target_reused_for_multiple_us2020_publications"] is True
    assert r["source_specific_author_links_use_different_legacy_targets"] is True
    assert r["author_link_target_difference_implies_distinct_article_packages"] is False

    assert r["published_replication_code_doi"] == "10.3886/spb3-g558"
    assert r["published_replication_code_doi_verified_independently"] is True
    assert r["record_43_to_published_replication_code_doi_linkage_verified"] is False
    assert r["article_specific_ade7138_public_replication_package_resolved"] is False
    assert r["sufficient_for_variable_dictionary_gate"] is False
    assert r["role"] == "REPLICATION_NAVIGATION_PROVENANCE_ONLY"

    assert "legacy_record_43_to_published_replication_code_doi_crosswalk" in audit["unresolved_blockers"]
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Author-facing replication navigation locators" in text
    assert "record 43" in text
    assert "does not establish that record 43 is the DOI package" in text


def test_replication_code_two_stage_pipeline_does_not_substitute_for_release_dictionary() -> None:
    audit = load(CONTRACT)
    r = audit["replication_code_two_stage_scope_boundary"]

    assert r["research_specific_platform_tables_created"] is True
    assert r["academic_team_had_direct_access_to_meta_internal_logs"] is False
    assert r["code_pipeline_two_stage_structure_verified"] is True
    assert r["stage_1_role"] == "GENERATE_RESEARCH_SPECIFIC_PLATFORM_USAGE_TABLES_FROM_META_INTERNAL_DATA"
    assert r["stage_1_written_and_executed_by_meta_employees"] is True
    assert r["stage_1_reviewed_by_academic_team"] is True
    assert r["stage_2_role"] == "PREPROCESS_AND_ANALYZE_RESEARCH_SPECIFIC_TABLES"
    assert r["stage_2_academic_team_could_write_execute_and_modify"] is True
    assert r["faq_confirms_replication_data_and_code_archived_at_somar_icpsr_vde"] is True
    assert r["faq_confirms_archived_platform_wide_data_are_aggregated_as_shared_with_academic_team"] is True
    assert r["archived_replication_package_contains_complete_stage_1_table_generation_code_verified"] is False
    assert r["archived_replication_package_contains_current_300450_300470_release_schema_verified"] is False
    assert r["archived_replication_package_contains_exact_current_physical_columns_verified"] is False
    assert r["replication_code_alone_sufficient_to_infer_release_schema_without_inspection"] is False
    assert r["replication_code_alone_sufficient_to_pass_variable_dictionary_gate"] is False

    assert "replication_archive_stage_1_table_generation_code_scope" in audit["unresolved_blockers"]
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Two-stage replication-code scope boundary" in text
    assert "does **not** establish that the archived package contains the complete upstream table-generation layer" in text


def test_derived_segregation_aggregation_rules_do_not_leak_into_base_release_fields() -> None:
    audit = load(CONTRACT)
    b = audit["derived_segregation_aggregation_scope_boundary"]

    assert b["derived_table_exposed_audience_disclosure"] == "SUM_OF_VIEWS"
    assert b["derived_table_can_count_same_user_multiple_times_across_posts_or_days"] is True
    assert b["current_300470_catalog_lists_content_views_and_audience_size_separately"] is True
    assert b["current_300450_catalog_lists_potential_audience_size"] is True
    assert b["derived_table_rules_verified_as_current_300470_release_rules"] is False
    assert b["derived_table_rules_verified_as_current_300450_release_rules"] is False
    assert b["derived_exposed_sum_of_views_equivalent_to_current_300470_audience_size"] is False
    assert b["derived_exposed_sum_of_views_usable_as_r_view_numerator"] is False
    assert b["derived_potential_aggregation_usable_as_r_view_denominator"] is False
    assert b["cross_table_semantic_substitution_authorized"] is False
    assert b["exact_target_dictionary_mapping_required"] is True
    assert "derived_segregation_table_aggregation_not_mappable_to_base_release_fields" in audit["unresolved_blockers"]
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Derived segregation-table aggregation boundary" in text
    assert "must not be imported into 300450 or 300470" in text


def test_support_escalation_is_public_documentation_only_and_non_evidentiary() -> None:
    audit = load(CONTRACT)
    s = audit["official_documentation_support_escalation"]

    assert s["escalation_ready"] is True
    assert s["support_request_sent_in_this_audit"] is False
    assert s["restricted_data_or_vde_access_requested"] is False
    assert s["requested_items"] == [
        "ICPSR_300450_CURRENT_V2_PUBLIC_DATA_DICTIONARY_DIRECT_DOWNLOAD_OR_FILE_IDENTITY",
        "ICPSR_300470_CURRENT_VERSION_NUMBER_AND_VERSION_SPECIFIC_DOI",
        "ICPSR_300470_CURRENT_VERSION_HISTORY_OR_CITATION_SURFACE",
        "ICPSR_300470_PUBLIC_DATA_DICTIONARY_OR_VARIABLE_DESCRIPTIONS_DIRECT_DOWNLOAD_OR_FILE_IDENTITY",
        "CONFIRM_CURRENT_PUBLIC_DOCUMENTATION_LOCATION_FOR_BOTH_TARGET_STUDIES",
        "ICPSR_300450_CURRENT_ROW_INCLUSION_ELIGIBILITY_AND_ABSENT_ROW_DOCUMENTATION_LOCATION",
        "ICPSR_300470_CURRENT_ROW_INCLUSION_ELIGIBILITY_AND_ABSENT_ROW_DOCUMENTATION_LOCATION",
        "CURRENT_DOCUMENTATION_LOCATION_FOR_SHARED_ELIGIBLE_INVENTORY_RELATION_IF_DOCUMENTED",
    ]
    assert "REQUEST_PUBLIC_DOCUMENTATION_ONLY" in s["request_constraints"]
    assert "DO_NOT_REQUEST_RESTRICTED_DATA" in s["request_constraints"]
    assert "DO_NOT_REQUEST_VDE_ACCESS" in s["request_constraints"]
    assert s["support_reply_alone_without_target_specific_document_or_identifier_sufficient_for_gate"] is False
    assert s["official_reply_or_linked_artifact_must_be_archived_in_audit_before_state_change"] is True
    assert s["numerical_pairing_remains_blocked_until_document_contents_inspected"] is True
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Support escalation package" in text
    assert "public documentation only" in text


def test_support_request_draft_is_ready_but_not_sent() -> None:
    audit = load(CONTRACT)
    req = audit["support_request_draft"]

    assert req["recipient"] == "somar-help@umich.edu"
    assert req["status"] == "READY_NOT_SENT"
    assert req["send_authorized"] is False
    assert req["sent_in_this_audit"] is False
    assert req["manual_public_documentation_route_must_be_attempted_first"] is True
    assert req["send_precondition_satisfied"] is False
    assert req["public_documentation_only"] is True
    assert req["restricted_data_requested"] is False
    assert req["vde_access_requested"] is False
    assert req["asks_support_to_infer_variable_names"] is False
    assert req["asks_support_to_calculate_r_view"] is False
    assert req["asks_support_to_treat_legacy_as_current"] is False
    assert req["asks_support_to_interpret_shared_inventory"] is False
    assert req["target_studies"] == ["300450", "300470"]
    assert "current public documentation" in req["body"]
    assert "https://doi.org/10.3886/ICPSR300470" in req["body"]
    assert "current version number and version-specific DOI" in req["body"]
    assert "not requesting restricted data or Virtual Data Enclave access" in req["body"]
    assert "row inclusion/eligibility" in req["body"]
    assert "meaning of a URL row being absent" in req["body"]
    assert "not for SOMAR to make an interpretive determination" in req["body"]
    assert "ICPSR_300470_CURRENT_VERSION_NUMBER_AND_VERSION_SPECIFIC_DOI_OR_VERSION_HISTORY_CITATION_SURFACE" in req["requested_evidence"]
    assert req["response_handling"]["support_reply_by_itself_passes_gate"] is False
    assert req["response_handling"]["target_specific_official_link_or_identifier_required"] is True
    assert req["response_handling"]["linked_artifact_must_be_archived_and_inspected_before_state_change"] is True
    assert req["response_handling"]["numerical_pairing_remains_blocked_until_document_contents_inspected"] is True
    assert req["response_handling"]["shared_inventory_compatibility_remains_unverified_until_linked_documentation_inspected"] is True
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Prepared SOMAR Help request — not sent" in text
    assert "READY_NOT_SENT" in text


def test_data_dictionary_is_explicit_field_level_authority_but_gate_remains_negative() -> None:
    audit = load(CONTRACT)
    d = audit["data_dictionary_semantic_authority"]

    assert d["source_type"] == "US2020_PROJECT_CODEBOOK_DOCUMENTATION_ARCHITECTURE"
    assert d["per_dataset_dictionary_declared"] is True
    assert d["declared_dictionary_fields"] == [
        "variable_name",
        "description",
        "type",
        "group",
        "map_keys",
        "aggregation_methods",
        "disclosures",
    ]
    assert d["exact_variable_name_source"] is True
    assert d["aggregation_method_source"] is True
    assert d["disclosure_source"] is True
    assert d["codebook_prose_substitutes_for_dictionary_rows"] is False
    assert d["proves_current_300450_300470_file_identity"] is False
    assert d["sufficient_for_variable_dictionary_gate"] is False
    assert d["intended_role"] == "FIELD_LEVEL_DOCUMENTATION_AUTHORITY"
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Data-dictionary semantic authority" in text
    assert "map keys" in text
    assert "cannot substitute for those rows" in text


def test_v3_exposure_potential_scope_asymmetry_forbids_cross_inference() -> None:
    audit = load(CONTRACT)
    a = audit["legacy_v3_exposure_potential_scope_asymmetry"]

    assert a["exposure_declared_level"] == "URL"
    assert a["exposure_overview_column_scope"] == "SPECIFIC_URL"
    assert a["exposure_overview_scope_consistent"] is True
    assert a["potential_exposure_declared_level"] == "URL"
    assert a["potential_exposure_overview_column_scope"] == "SPECIFIC_DOMAIN"
    assert a["potential_exposure_overview_scope_consistent"] is False
    assert a["same_v3_codebook_contains_asymmetric_scope_wording"] is True
    assert a["exposure_fix_transferable_to_potential_exposure_by_inference"] is False
    assert a["denominator_scope_resolved"] is False
    assert a["numerator_disclosure_semantics_resolved"] is False
    assert a["numerical_pairing_authorized"] is False
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "V3 Exposure/Potential-Exposure scope asymmetry" in text
    assert "cannot be transferred to Potential Exposure by analogy" in text


def test_science_unique_audience_sets_do_not_authorize_release_audience_size_substitution() -> None:
    audit = load(CONTRACT)
    b = audit["science_unique_audience_release_metric_boundary"]

    assert b["paper_funnel_orders_potential_before_exposed"] is True
    assert b["paper_inventory_precedes_algorithmic_curation"] is True
    assert b["conceptual_exposed_subset_of_potential_supported"] is True
    assert b["candidate_ratio_unique_user_interpretation"] == "EXPOSED_UNIQUE_USERS_DIVIDED_BY_POTENTIAL_UNIQUE_USERS"
    assert b["legacy_codebook_contains_multi_counting_audience_rules"] is True
    assert b["legacy_multi_counting_rules_scope_to_exact_target_url_release_verified"] is False
    assert b["current_release_audience_size_unique_user_semantics_verified"] is False
    assert b["current_release_audience_size_deduplicated_over_full_study_period_verified"] is False
    assert b["current_release_metric_equivalent_to_paper_unique_user_set_size_verified"] is False
    assert b["r_view_interpretable_as_probability_or_fraction_of_potential_users_from_release_fields"] is False
    assert b["exact_dictionary_mapping_required"] is True
    assert b["numerical_pairing_authorized"] is False
    assert "paper_unique_user_set_to_release_audience_metric_equivalence" in audit["unresolved_blockers"]
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Science unique-audience vs release-metric boundary" in text
    assert "CONCEPTUAL_UNIQUE_USER_FUNNEL_VERIFIED / RELEASE_METRIC_EQUIVALENCE_UNVERIFIED" in text


def test_v3_row_universe_asymmetry_forbids_naive_inner_join() -> None:
    audit = load(CONTRACT)
    r = audit["legacy_v3_url_row_universe_asymmetry"]

    assert r["common_level"] == "URL"
    assert r["common_population"] == "US_ADULT_MONTHLY_ACTIVE_USERS"
    assert r["common_period"] == "2020-09-01/2021-02-01"
    assert r["common_inclusion_filters"] == [
        "CLASSIFIED_CIVIC_AND_NEWS_BY_META_INTERNAL_CLASSIFIERS",
        "SHARED_MORE_THAN_100_TIMES_TO_FACEBOOK_BY_US_USERS_DURING_STUDY_PERIOD",
    ]
    assert r["potential_specific_inclusion"] == "POTENTIALLY_VIEWED_BY_US_USERS_IN_FEED_BECAUSE_SHARED_BY_US_BASED_CONNECTION"
    assert r["exposure_specific_inclusion"] == "VIEWED_BY_US_USERS_IN_FEED"
    assert r["row_universe_identity_verified"] is False
    assert r["exposure_rows_guaranteed_for_every_potential_row"] is False
    assert r["absent_exposure_row_equivalent_to_zero_exposed_audience_verified"] is False
    assert r["inner_join_preserves_zero_exposure_urls_verified"] is False
    assert r["default_inner_join_authorized"] is False
    assert r["missing_or_absent_row_policy_required"] is True
    assert "legacy_potential_exposure_and_exposure_row_universes_not_guaranteed_identical" in audit["unresolved_blockers"]
    assert "absent_exposure_row_zero_interpretation" in audit["unresolved_blockers"]
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "V3 URL row-universe asymmetry" in text
    assert "NAIVE_INNER_JOIN_FORBIDDEN" in text


def test_record_34_manifest_does_not_prove_record_32_36_attachment() -> None:
    audit = load(CONTRACT)
    a = audit["legacy_documentation_attachment_scope"]

    assert a["direct_manifest_record"] == "34"
    assert a["direct_attachment_to_record_34_verified"] is True
    assert a["legacy_record_32_multiple_files_indexed"] is True
    assert a["legacy_record_36_multiple_files_indexed"] is True
    assert a["legacy_record_32_codebook_label_indexed"] == "US2020_FB&IG_Elections_External_Codebook"
    assert a["legacy_record_36_codebook_label_indexed"] == "US2020_FB&IG_Elections_External_Codebook"
    assert a["target_records_multi_file_availability_supported"] is True
    assert a["target_records_exact_documentation_file_identity_verified"] is False
    assert a["same_uuid_attachment_to_record_32_verified"] is False
    assert a["same_uuid_attachment_to_record_36_verified"] is False
    assert a["record_34_manifest_sufficient_for_exposure_record_32_file_identity"] is False
    assert a["record_34_manifest_sufficient_for_potential_record_36_file_identity"] is False
    assert a["search_nonrecovery_interpretable_as_absence"] is False
    assert a["current_2026_attachment_or_byte_identity_verified"] is False
    assert a["role"] == "RECORD_34_DIRECT_ATTACHMENT_ONLY_OTHER_LEGACY_TARGET_ATTACHMENTS_UNVERIFIED"
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Legacy documentation attachment scope" in text
    assert "TARGET_RECORDS_MULTIPLE_FILES_VERIFIED / RECORD_34_EXACT_UUID_ATTACHMENT_VERIFIED / RECORD_32_36_SAME_UUID_ATTACHMENT_UNVERIFIED / CURRENT_LINKAGE_UNVERIFIED" in text



def test_glossary_separates_audience_users_from_content_view_events() -> None:
    audit = load(CONTRACT)
    g = audit["legacy_glossary_audience_view_semantics"]

    assert g["source_type"] == "INDEXED_US2020_GLOSSARY_SPREADSHEET_VIEW"
    assert g["audience_is_user_count"] is True
    assert g["content_views_is_screen_appearance_count"] is True
    assert g["audience_and_content_views_are_distinct_estimands"] is True
    assert g["content_views_admissible_as_r_view_numerator"] is False
    assert g["potential_audience_connection_inventory_semantics_verified"] is True
    assert g["potential_audience_population_scope_verified"] == "ADULT_US_MONTHLY_ACTIVE_USERS"
    assert g["potential_audience_definition_supports_denominator_concept"] is True
    assert g["potential_audience_definition_establishes_physical_denominator_field"] is False
    assert g["glossary_establishes_target_physical_column_names"] is False
    assert g["glossary_establishes_target_release_aggregation_deduplication"] is False
    assert g["glossary_establishes_current_2026_release_linkage"] is False
    assert g["exact_dictionary_mapping_still_required"] is True
    assert g["numerical_pairing_authorized"] is False
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "US2020 Glossary audience/view semantic distinction" in text
    assert "AUDIENCE_USER_COUNT_VS_VIEW_EVENT_COUNT_VERIFIED / TARGET_RELEASE_FIELD_MAPPING_UNVERIFIED" in text


def test_science_funnel_does_not_silently_prove_raw_release_shared_inventory() -> None:
    audit = load(CONTRACT)
    b = audit["science_inventory_release_scope_boundary"]

    assert b["paper_actual_exposure_is_subset_of_inventory"] is True
    assert b["paper_funnel_shared_inventory_verified"] is True
    assert b["potential_release_requires_connection_based_eligibility"] is True
    assert b["exposure_release_description_requires_view_in_feed"] is True
    assert b["exposure_release_description_explicitly_requires_connection_based_eligibility"] is False
    assert b["project_glossary_feed_can_include_suggested_posts"] is True
    assert b["raw_release_shared_inventory_verified"] is False
    assert b["raw_exposure_audience_subset_of_raw_potential_audience_verified"] is False
    assert b["paper_analysis_subset_relation_transferable_to_raw_release_fields_without_mapping"] is False
    assert b["candidate_r_view_requires_shared_inventory_compatibility"] is True
    assert b["numerical_pairing_authorized"] is False
    assert "paper_shared_inventory_to_release_field_scope_equivalence" in audit["unresolved_blockers"]
    q = audit["candidate_component_quantity"]
    assert q["status"] == "CONCEPTUALLY_CONDITIONAL_ON_SHARED_INVENTORY_NUMERICALLY_BLOCKED"
    assert q["current_release_shared_inventory_verified"] is False
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Science inventory funnel vs release-field scope" in text
    assert "CONCEPTUALLY_CONDITIONAL_ON_SHARED_INVENTORY" in text


def test_deleted_page_rule_is_not_imported_into_target_url_pair() -> None:
    audit = load(CONTRACT)
    assert "legacy_potential_audience_deleted_page_exclusion" not in audit
    assert any("target-specific applicability" in x for x in audit["interpretation_boundary"])
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Scope correction: deleted-Page potential-audience rule" in text
    assert "NON_TARGET_SCOPE_RULE_NOT_IMPORTED" in text


def test_legacy_source_link_rot_is_recorded_without_changing_scientific_gate() -> None:
    audit = load(CONTRACT)
    r = audit["legacy_source_live_retrieval_state"]

    assert r["verified_on"] == "2026-09-25"
    assert len(r["tested_urls"]) == 5
    assert r["redirect_target"] == "https://www.icpsr.umich.edu/sites/somar/home"
    assert r["tested_legacy_urls_now_redirect_to_current_somar_home"] is True
    assert r["original_artifact_bytes_retrievable_through_tested_current_public_web_surface"] is False
    assert r["historical_indexed_evidence_retained"] is True
    assert r["redirect_invalidates_previously_recovered_historical_content"] is False
    assert r["current_live_retrieval_role"] == "NONE"
    assert r["scientific_gate_changed"] is False
    assert r["role"] == "LEGACY_INDEXED_PROVENANCE_LINK_ROT_RECORDED"
    assert audit["numerical_calculation_authorized"] is False
    assert audit["empirical_promotion_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Legacy source live-retrieval state" in text
    assert "LEGACY_INDEXED_PROVENANCE_RETAINED / ORIGINAL_URLS_REDIRECT" in text


def test_current_study_page_shell_state_does_not_reverse_recovered_evidence() -> None:
    audit = load(CONTRACT)
    s = audit["current_study_page_live_retrieval_state"]

    assert s["verified_on"] == "2026-09-25"
    assert s["potential_exposure_study"] == "300450"
    assert s["exposure_study"] == "300470"
    assert s["potential_exposure_direct_page_content_retrievable_in_current_audited_html"] is False
    assert s["exposure_direct_page_content_retrievable_in_current_audited_html"] is False
    assert s["direct_pages_expose_client_side_shell_only"] is True
    assert s["current_catalog_search_exposes_both_study_descriptions"] is True
    assert s["prior_indexed_300450_v2_doi_and_dictionary_offer_retained_as_recovered_official_evidence"] is True
    assert s["prior_indexed_300450_evidence_invalidated_by_current_shell_behavior"] is False
    assert s["current_exact_search_recovered_300450_doi_dictionary_block"] is True
    assert s["current_exact_search_recovered_300470_doi_dictionary_block"] is False
    assert s["current_300470_doi_version_recovered"] is False
    assert s["current_300470_dictionary_contents_recovered"] is False
    assert s["current_live_retrieval_failure_interpretable_as_documentation_absence"] is False
    assert s["scientific_gate_changed"] is False
    assert audit["current_collection_identity"]["potential_exposure"]["doi"] == "10.3886/ICPSR300450.V2"
    assert audit["current_collection_identity"]["exposure"]["doi"] is None
    assert audit["numerical_calculation_authorized"] is False

    text = DOC.read_text(encoding="utf-8")
    assert "Current study-page live retrieval state" in text
    assert "CURRENT_300450_INDEXED_EVIDENCE_RECONFIRMED" in text
