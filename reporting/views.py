from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from reporting.forms import UserForm
from reporting.models import ReportItem, Report, IDLUser
from django.contrib import messages

@login_required(login_url='/login/')
def index(request):
	if request.POST:
		# get the filters here from the form
		min_date = request.POST['min_date']
		max_date = request.POST['max_date']
		filter_tags = request.POST.getlist('filter_tags')
		filter_authors = request.POST.getlist('filter_authors')
		report_items = ReportItem.objects.filter(
			created_at__gte=min_date,
			created_at__lte=max_date,
			
			)
		if len(filter_tags) > 0:
			report_items = report_items.filter(
				tags__id__in=filter_tags,
				)
		if len(filter_authors) > 0:
			report_items = report_items.filter(
				created_by__id__in=filter_authors
				)
		report_items = report_items.distinct()
	else:
		report_items = ReportItem.objects.all()
	data = {
		'tags': Tag.objects.all(),
		'authors': IDLUser.objects.filter(is_active=True),
		'report_items': report_items,
		'reports': Report.objects.all()
	}
	return render_to_response('reporting/index.html', data, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def save_report(request):
	if request.POST:
		# get the filters here from the form
		name = request.POST['report_name']
		description = request.POST['report_description']
		min_date = request.POST['min_date']
		max_date = request.POST['max_date']
		filter_tags = request.POST.getlist('filter_tags')
		filter_authors = request.POST.getlist('filter_authors')
		report_items = ReportItem.objects.filter(
			created_at__gte=min_date,
			created_at__lte=max_date,
			
			)
		if len(filter_tags) > 0:
			report_items = report_items.filter(
				tags__id__in=filter_tags,
				)
		if len(filter_authors) > 0:
			report_items = report_items.filter(
				created_by__id__in=filter_authors
				)
		report_items = report_items.distinct()
		if report_items.count() > 0:
			report = Report()
			report.created_by = request.user
			report.name = name
			report.description = description
			try:
				report.save()
				report.report_items.add(*report_items)
				# TODO: add the parameter
				return redirect('reporting:view_report', pk=report.id)
			except:
				messages.error(request, "Failed to save report")
		else:
			messages.error(request, "Report was empty. Did not save.")
		return redirect('reporting:index')


@login_required(login_url='/login/')
def delete_report(request, pk):
	report = Report.objects.get(pk=int(pk))
	report.delete()
	return redirect('reporting:index')

@login_required(login_url='/login/')
def delete_tag(request, pk):
	bad_tag = Tag.objects.get(pk=int(pk))
	tagged_items = ReportItem.objects.filter(tags__id__in=pk)
	for item in tagged_items:
		item.tags.remove(bad_tag)
	bad_tag.delete()
	return redirect('reporting:index')

@login_required(login_url='/login/')
def view_report(request, pk):
	report = Report.objects.get(pk=int(pk))
	data = {
		'report': report,
		'report_items': report.report_items.all().order_by('created_at')
	}
	return render_to_response('reporting/view_report.html', data, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def save_item(request):
	if request.POST:
		required_fields = ['report_item_description', 'report_item_tags']
		for field in required_fields:
			if field not in request.POST:
				messages.error(request, 'Invalid Form.')
				return redirect('reporting:index')
		if request.POST['report_item_description'] == "":
			messages.warning(request, 'Please fill all fields.')
			return redirect('reporting:index')

		description = request.POST['report_item_description']
		tags_string = request.POST['report_item_tags']
		tags = [tag.strip() for tag in tags_string.split(',')]
		item = ReportItem()
		item.created_by = request.user
		item.content = description
		item.save()
		for tag in tags:
			item.tags.add(tag)

	messages.success(request, 'Added a report item')
	return redirect('reporting:index')

@login_required(login_url='/login/')
def edit_item(request, pk):
	report_item = ReportItem.objects.get(pk=int(pk))
	report_item_tags = report_item.tags.names()
	tags = ", " .join(report_item_tags)
	data ={
		'report_item': report_item,
		'tags': tags,
	}

	return render_to_response('reporting/edit_item.html', data, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def save_edit_item(request, pk):
	if request.POST:
		required_fields = ['report_edit_item_description', 'report_edit_item_tags']
		for field in required_fields:
			if field not in request.POST:
				messages.error(request, 'Invalid Form.')
				return redirect('reporting:index')
		if request.POST['report_edit_item_description'] == "":
			messages.warning(request, 'Please fill all fields.')
			return redirect('reporting:index')

		description = request.POST['report_edit_item_description']
		tags_string = request.POST['report_edit_item_tags']
		tags = [tag.strip() for tag in tags_string.split(',')]
		item = ReportItem.objects.get(pk=int(pk))
		item.created_by = request.user
		item.content = description
		item.save()
		item.tags.clear()
		for tag in tags:
			item.tags.add(tag)

	messages.success(request, 'Edited a report item')
	return redirect('reporting:index')