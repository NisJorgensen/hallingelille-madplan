import unicodecsv as csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.admin.util import label_for_field

def export_as_csv(description="Download selected rows as CSV file",header=True):
    """
    This function returns an export csv action
    This function ONLY downloads the columns shown in the list_display of the admin
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/ and /2020/
        """
        # TODO Also create export_as_csv for exporting all columns including list_display
        if not request.user.is_staff:
            raise PermissionDenied
        opts = modeladmin.model._meta
        field_names = modeladmin.list_display
        if 'action_checkbox' in field_names:
            field_names.remove('action_checkbox')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            headers = []
            for field_name in list(field_names):
                label = label_for_field(field_name,modeladmin.model,modeladmin)
                if unicode.islower(label):
                   label = unicode.title(label)
                headers.append(label)
            writer.writerow(headers)
        for row in queryset:
            values = []
            for field in field_names:
                value = (getattr(row, field))
                if callable(value):
                    try:
                        value = value() or ''
                    except:
                        value = 'Error retrieving value'
                if value is None:
                    value = ''
                values.append(unicode(value).encode('utf-8'))
            writer.writerow(values)
        return response

    export_as_csv.short_description = description
    return export_as_csv

