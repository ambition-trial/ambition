
.. code-block:: sql

	INSERT INTO ambition_ae_deathreport (revision, created, modified, user_created, user_modified, hostname_created, hostname_modified, device_created, device_modified, id, subject_identifier, tracking_identifier, action_identifier, parent_action_identifier, related_action_identifier, action_item_reason, report_datetime, death_datetime, study_day, death_as_inpatient, cause_of_death_other, narrative, cause_of_death_old, tb_site, action_item_id, cause_of_death_id, parent_action_item_id, related_action_item_id, site_id)
	select revision, created, modified, user_created, user_modified, hostname_created, hostname_modified, device_created, device_modified, id, subject_identifier, tracking_identifier, action_identifier, parent_action_identifier, related_action_identifier, action_item_reason, report_datetime, death_datetime, study_day, death_as_inpatient, cause_of_death_other, narrative, cause_of_death_old, tb_site, action_item_id, cause_of_death_id, parent_action_item_id, related_action_item_id, site_id
	from ambition_prn_deathreport order by created;


.. code-block:: sql

	INSERT INTO ambition_ae_historicaldeathreport (history_id, history_date, history_change_reason, history_type, history_user_id, revision, created, modified, user_created, user_modified, hostname_created, hostname_modified, device_created, device_modified, id, subject_identifier, tracking_identifier, action_identifier, parent_action_identifier, related_action_identifier, action_item_reason, report_datetime, death_datetime, study_day, death_as_inpatient, cause_of_death_other, narrative, cause_of_death_old, tb_site, action_item_id, cause_of_death_id, parent_action_item_id, related_action_item_id, site_id)
	select history_id, history_date, history_change_reason, history_type, history_user_id, revision, created, modified, user_created, user_modified, hostname_created, hostname_modified, device_created, device_modified, id, subject_identifier, tracking_identifier, action_identifier, parent_action_identifier, related_action_identifier, action_item_reason, report_datetime, death_datetime, study_day, death_as_inpatient, cause_of_death_other, narrative, cause_of_death_old, tb_site, action_item_id, cause_of_death_id, parent_action_item_id, related_action_item_id, site_id
	from ambition_prn_historicaldeathreport order by created;


.. code-block:: sql

	update ambition_prn_deathreporttmg set action_item_id=NULL where action_item_id='687ecfbfb1084ad09141b7827c902a83';


.. code-block:: sql

	INSERT INTO ambition_ae_deathreporttmg (created, modified, user_created, user_modified, hostname_created, hostname_modified, revision, device_created, device_modified, id, report_status, report_closed_datetime, subject_identifier, tracking_identifier, action_identifier, report_datetime, cause_of_death_old, cause_of_death_other, cause_of_death_agreed, tb_site, narrative, death_report_id, site_id, parent_action_identifier, related_action_identifier, action_item_id, parent_action_item_id, related_action_item_id, action_item_reason, cause_of_death_id)
	select created, modified, user_created, user_modified, hostname_created, hostname_modified, revision, device_created, device_modified, id, report_status, report_closed_datetime, subject_identifier, tracking_identifier, action_identifier, report_datetime, cause_of_death_old, cause_of_death_other, cause_of_death_agreed, tb_site, narrative, death_report_id, site_id, parent_action_identifier, related_action_identifier, action_item_id, parent_action_item_id, related_action_item_id, action_item_reason, cause_of_death_id
	from ambition_prn_deathreporttmg order by created;


.. code-block:: sql

	INSERT INTO ambition_ae_historicaldeathreporttmg (history_id, history_date, history_change_reason, history_type, history_user_id, created, modified, user_created, user_modified, hostname_created, hostname_modified, revision, device_created, device_modified, id, report_status, report_closed_datetime, subject_identifier, tracking_identifier, action_identifier, report_datetime, cause_of_death_old, cause_of_death_other, cause_of_death_agreed, tb_site, narrative, death_report_id, site_id, parent_action_identifier, related_action_identifier, action_item_id, parent_action_item_id, related_action_item_id, action_item_reason, cause_of_death_id)
	select history_id, history_date, history_change_reason, history_type, history_user_id, created, modified, user_created, user_modified, hostname_created, hostname_modified, revision, device_created, device_modified, id, report_status, report_closed_datetime, subject_identifier, tracking_identifier, action_identifier, report_datetime, cause_of_death_old, cause_of_death_other, cause_of_death_agreed, tb_site, narrative, death_report_id, site_id, parent_action_identifier, related_action_identifier, action_item_id, parent_action_item_id, related_action_item_id, action_item_reason, cause_of_death_id
	from ambition_prn_historicaldeathreporttmg order by created;


.. code-block:: sql

	update edc_action_item_actionitem set reference_model="ambition_ae.deathreport" where reference_model="ambition_prn.deathreport";
	update edc_action_item_actionitem set reference_model="ambition_ae.deathreporttmg" where reference_model="ambition_prn.deathreporttmg";
	update edc_action_item_actionitem set reference_model="ambition_ae.deathreporttmgsecond" where reference_model="ambition_prn.deathreporttmgsecond";


.. code-block:: sql

	update edc_action_item_actionitem set related_reference_model="ambition_ae.deathreport" where related_reference_model="ambition_prn.deathreport";
	update edc_action_item_actionitem set related_reference_model="ambition_ae.deathreporttmg" where related_reference_model="ambition_prn.deathreporttmg";
	update edc_action_item_actionitem set related_reference_model="ambition_ae.deathreporttmgsecond" where related_reference_model="ambition_prn.deathreporttmgsecond";


.. code-block:: sql

	update edc_registration_registeredsubject set randomizationlist_model="ambition_rando.randomizationlist";