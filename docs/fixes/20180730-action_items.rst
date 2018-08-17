Fix action items created before version
---------------------------------------

This is a once-off fix.

List action items

.. code-block:: sql

	select t.name, a.action_identifier, a.parent_reference_identifier,
	a.parent_reference_model, a.related_reference_identifier,
	a.related_reference_model,a.linked_to_reference as linked,a.status,a.created
	from edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	where parent_reference_identifier is not null
	order by t.name;

Notice identifier fields other than ``ation_identifier`` list ``tracking identifier`` and action identifiers.


.. code-block:: sql

	select t.name, a.action_identifier, a.parent_reference_identifier, a.parent_reference_model, 
	br.action_identifier as BR,
	a.linked_to_reference as linked,a.status,a.created 
	from edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	left join ambition_subject_bloodresult as br on br.tracking_identifier=a.parent_reference_identifier
	where a.parent_reference_identifier is not null
	order by t.name;


.. code-block:: python

    from edc_action_item.models import ActionItem
    from ambition_subject.models import BloodResult

    for action_item in ActionItem.objects.all():
        if action_item.parent_reference_identifier in [br.tracking_identifier for br in BloodResult.objects.all()]:
            # get the action identifier from BR using the tracking_identifier
            new_action_identifier = (
                BloodResult.objects.get(tracking_identifier=action_item.parent_reference_identifier).action_identifier)
            action_item.parent_reference_identifier = new_action_identifier
            action_item.save()


Run these python scripts

.. code-block:: python

    from edc_action_item.models import ActionItem
    from ambition_ae.models import AeInitial

    for action_item in ActionItem.objects.all():
        if action_item.parent_reference_identifier in [obj.tracking_identifier for obj in AeInitial.objects.all()]:
            # get the action identifier from AE using the tracking_identifier
            new_action_identifier = (
                AeInitial.objects.get(tracking_identifier=action_item.parent_reference_identifier).action_identifier)
            action_item.parent_reference_identifier = new_action_identifier
            action_item.save()


.. code-block:: python

    from edc_action_item.models import ActionItem
    from ambition_ae.models import AeFollowup

    for action_item in ActionItem.objects.all():
        if action_item.parent_reference_identifier in [obj.tracking_identifier for obj in AeFollowup.objects.all()]:
            # get the action identifier from AE using the tracking_identifier
            new_action_identifier = (
                AeFollowup.objects.get(tracking_identifier=action_item.parent_reference_identifier).action_identifier)
            action_item.parent_reference_identifier = new_action_identifier
            action_item.save()


.. code-block:: python

    from edc_action_item.models import ActionItem
    from ambition_ae.models import AeTmg

    for action_item in ActionItem.objects.all():
        if action_item.parent_reference_identifier in [obj.tracking_identifier for obj in AeTmg.objects.all()]:
            # get the action identifier from AE using the tracking_identifier
            new_action_identifier = (
                AeTmg.objects.get(tracking_identifier=action_item.parent_reference_identifier).action_identifier)
            action_item.parent_reference_identifier = new_action_identifier
            action_item.save()


.. code-block:: python

    from edc_action_item.models import ActionItem
    from edc_locator.models import SubjectLocator

    for action_item in ActionItem.objects.all():
        if action_item.parent_reference_identifier in [obj.tracking_identifier for obj in SubjectLocator.objects.all()]:
            # get the action identifier from AE using the tracking_identifier
            new_action_identifier = (
                SubjectLocator.objects.get(tracking_identifier=action_item.parent_reference_identifier).action_identifier)
            action_item.parent_reference_identifier = new_action_identifier
            action_item.save()


.. code-block:: python

    from edc_action_item.models import ActionItem
    from ambition_prn.models import StudyTerminationConclusion

    for action_item in ActionItem.objects.all():
        if action_item.parent_reference_identifier in [obj.tracking_identifier for obj in StudyTerminationConclusion.objects.all()]:
            # get the action identifier from AE using the tracking_identifier
            new_action_identifier = (
                StudyTerminationConclusion.objects.get(tracking_identifier=action_item.parent_reference_identifier).action_identifier)
            action_item.parent_reference_identifier = new_action_identifier
            action_item.save()


.. code-block:: python

    from edc_action_item.models import ActionItem
    from ambition_prn.models import StudyTerminationConclusionW10

    for action_item in ActionItem.objects.all():
        if action_item.parent_reference_identifier in [obj.tracking_identifier for obj in StudyTerminationConclusionW10.objects.all()]:
            # get the action identifier from AE using the tracking_identifier
            new_action_identifier = (
                StudyTerminationConclusionW10.objects.get(tracking_identifier=action_item.parent_reference_identifier).action_identifier)
            action_item.parent_reference_identifier = new_action_identifier
            action_item.save()


.. code-block:: python

    from edc_action_item.models import ActionItem
    from ambition_prn.models import DeathReport

    for action_item in ActionItem.objects.all():
        if action_item.parent_reference_identifier in [obj.tracking_identifier for obj in DeathReport.objects.all()]:
            # get the action identifier from AE using the tracking_identifier
            new_action_identifier = (
                DeathReport.objects.get(tracking_identifier=action_item.parent_reference_identifier).action_identifier)
            action_item.parent_reference_identifier = new_action_identifier
            action_item.save()


.. code-block:: python

    from edc_action_item.models import ActionItem
    from ambition_prn.models import DeathReportTmg

    for action_item in ActionItem.objects.all():
        if action_item.parent_reference_identifier in [obj.tracking_identifier for obj in DeathReportTmg.objects.all()]:
            # get the action identifier from AE using the tracking_identifier
            new_action_identifier = (
                DeathReportTmg.objects.get(tracking_identifier=action_item.parent_reference_identifier).action_identifier)
            action_item.parent_reference_identifier = new_action_identifier
            action_item.save()

Now switch to mysql

.. code-block:: sql

	select t.name, a.action_identifier, a.parent_reference_identifier, a.parent_reference_model, 
	a.related_reference_identifier, a.related_reference_model,
	a.linked_to_reference as linked,a.status,a.created 
	from edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	left join ambition_subject_bloodresult as br on br.action_identifier=a.parent_reference_identifier
	where a.parent_reference_identifier is not null
	and t.name='submit-ae-followup-report'
	and a.parent_reference_model='ambition_ae.aefollowup'
	order by t.name;



.. code-block:: sql

	select subject_identifier, t.name, a.action_identifier, a.parent_reference_identifier, a.parent_reference_model, 
	a.related_reference_identifier, a.related_reference_model,
	a.linked_to_reference as linked,a.status,a.created 
	from edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	where a.subject_identifier='092-10990017-2'
	order by t.name;


submit-study-termination-conclusion


.. code-block:: sql

	select subject_identifier, t.name, a.action_identifier, a.parent_reference_identifier, a.parent_reference_model, 
	a.related_reference_identifier, a.related_reference_model,
	a.linked_to_reference as linked,a.status,a.created 
	from edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	where t.name='submit-study-termination-conclusion'
	order by a.created;

Run these updates

.. code-block:: sql

	update edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	set a.related_reference_identifier=null
	where t.name='submit-study-termination-conclusion';

	update edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	set a.related_reference_identifier=null
	where a.parent_reference_model='ambition_subject.bloodresult';

	update edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	set a.related_reference_model='ambition_ae.aeinitial'
	where a.parent_reference_model='ambition_ae.aeinitial'
	and related_reference_identifier is not null;


	update edc_action_item_actionitem
	set related_reference_model='ambition_ae.aeinitial'
	where action_identifier='AC99-1807-2508-5033-506X';

.. code-block:: sql

	select subject_identifier, t.name, a.action_identifier, a.parent_reference_identifier, a.parent_reference_model, 
	a.related_reference_identifier, a.related_reference_model,
	a.linked_to_reference as linked,a.status,a.created 
	from edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	where a.related_reference_identifier is not null
	order by a.created;


Run this update for ``AC99-1807-0719-2824-27EV``

.. code-block:: sql

	update edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	set related_reference_identifier='AC99-1807-0719-2824-27EV'
	where parent_reference_identifier='AC99-1807-0719-2824-27EV';

Delete cancelled action-items

.. code-block:: sql

    delete from edc_action_item_actionitem where status='cancelled';

.. code-block:: sql

	select subject_identifier, t.name, a.action_identifier, a.parent_reference_identifier, a.parent_reference_model, 
	a.related_reference_identifier, a.related_reference_model,
	a.linked_to_reference as linked,a.status,a.created 
	from edc_action_item_actionitem as a
	left join edc_action_item_actiontype as t on t.id=a.action_type_id
	order by a.created;


Update linked_to_reference
++++++++++++++++++++++++++


.. code-block:: python

    from django.apps import apps as django_apps
    from django.db.models import ObjectDoesNotExist
    from edc_action_item.models import ActionItem
    from edc_constants.constants import OPEN, CLOSED, CANCELLED


    model_classes=[]

    for model_cls in django_apps.get_models():
        if model_cls._meta.app_label != 'edc_action_item':
            try:
                model_cls.action_identifier
            except AttributeError:
                pass
            else:
                if 'historical' not in model_cls._meta.label_lower:
                    model_classes.append(model_cls)
    
    for model_cls in model_classes:
        for obj in model_cls.objects.all():
            try:
                action_item = ActionItem.objects.get(
                    action_identifier=obj.action_identifier,
                    status__in=[OPEN, CLOSED],
                    linked_to_reference=False)
            except ObjectDoesNotExist as e:
                pass
            else:
                print(action_item, action_item.linked_to_reference)
                action_item.linked_to_reference = True
                action_item.save()


.. code-block:: python

    from edc_action_item.models import ActionItem
    from django.db.models import ObjectDoesNotExist

    for action_item in ActionItem.objects.filter(
            parent_reference_identifier__isnull=False).exclude(
                parent_reference_identifier__startswith='AC'):
        parent_reference_model_cls = django_apps.get_model(
            action_item.parent_reference_model)
        try:
            parent_action_identifier = parent_reference_model_cls.objects.get(
                tracking_identifier=action_item.parent_reference_identifier)
        except ObjectDoesNotExist as e:
            print(action_item.parent_reference_identifier, e)
        else:
            action_item.parent_reference_identifier = parent_action_identifier
            # action_item.save()
            print('saved parent_reference_identifier', action_item)

    for action_item in ActionItem.objects.filter(
            related_reference_identifier__isnull=False).exclude(
                related_reference_identifier__startswith='AC'):
        related_reference_model_cls = django_apps.get_model(
            action_item.parent_reference_model)
        try:
            related_action_identifier = related_reference_model_cls.objects.get(
                tracking_identifier=action_item.related_reference_identifier)
        except ObjectDoesNotExist as e:
            print(action_item.parent_reference_identifier, e)
        else:
            action_item.related_reference_identifier = related_action_identifier
            # action_item.save()
            print('saved related_reference_identifier', action_item)
