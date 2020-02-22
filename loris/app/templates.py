"""templates
"""

from flask import render_template, request, flash, url_for, redirect, \
    send_from_directory, session
from flask_login import current_user
import datajoint as dj
from ast import literal_eval

from loris import config
from loris.app.forms.dynamic_form import DynamicForm
from loris.app.utils import user_has_permission, save_join, get_jsontable


def joined_table_template(
    table_names, name='Joined Table', redirect_url='#',
    message='None'
):
    """template for joined tables
    """

    if redirect_url != '#':
        redirect_url = url_for(redirect_url)

    tables = []
    for table_name in table_names:
        if not isinstance(table_name, str):
            tables.append(table_name)
        else:
            tables.append(config.get_table(table_name))

    joined_table = save_join(tables)
    df = joined_table.proj().fetch(format='frame').reset_index()
    data = get_jsontable(
        df, joined_table.heading.primary_key
    )

    return render_template(
        'pages/joined_table.html',
        name=name,
        url=redirect_url,
        data=data,
        toggle_off_keys=[0],
        message=message
    )


def form_template(
    schema, table, subtable, edit_url, overwrite_url, page='table',
    join_tables=None, joined_name=None, redirect_page=None,
    override_permissions=False, **kwargs
):
    """template for rendering tables with forms
    """

    if current_user.user_name in config['administrators']:
        readonly = []
    else:
        readonly = [config['user_name']]
        kwargs[config['user_name']] = current_user.user_name

    if redirect_page is None:
        redirect_page = page

    # showing
    enter_show = ['', 'false']
    # get id if it exists (will be restriction)
    _id = literal_eval(request.args.get('_id', "None"))
    # get table and create dynamic form
    table_class = getattr(config['schemata'][schema], table)
    # get table name
    table_name = '.'.join([schema, table])

    # test if user has permissions
    if _id is not None and not override_permissions:
        truth = user_has_permission(table_class & _id, current_user.user_name)
        if not truth:
            flash(
                f'User {current_user.user_name} does not have permission '
                f'to overwrite or edit entry: {_id}', 'error')
            return redirect(
                url_for(
                    redirect_page,
                    table=table,
                    schema=schema,
                    subtable=subtable,
                    _id=None
                )
            )

    # if not passed directly
    if not (subtable is None or subtable == 'None'):
        table_name = f'{table_name}.{subtable}'
        table_class = getattr(table_class, subtable)

    # standard delete and edit urls
    delete_url = url_for(
        'delete', schema=schema, table=table, subtable=subtable)

    overwrite = request.args.get('overwrite', "False")
    edit = request.args.get('edit', "False")
    dynamicformclass = DynamicForm

    dynamicform, form = config.get_dynamicform(
        table_name, table_class, dynamicformclass, **kwargs
    )

    filename = dynamicform.draw_relations()

    # load/notload table
    data = dynamicform.get_jsontable(
        edit_url, delete_url, overwrite_url,
        join_tables, joined_name
    )

    toggle_off_keys = [0]

    if request.method == 'POST':
        submit = request.form.get('submit', None)

        form.rm_hidden_entries()

        if submit is None:
            pass

        elif submit in ['Save', 'Overwrite', 'Edit']:
            # show enter fields
            enter_show = ['show', 'true']

            if form.validate_on_submit():
                kwargs = {}
                if submit == 'Overwrite':
                    kwargs['replace'] = True

                try:
                    _id = dynamicform.insert(
                        form,
                        (_id if overwrite == 'False' else None),
                        **kwargs)
                except dj.DataJointError as e:
                    flash(f"{e}", 'error')
                else:
                    dynamicform.reset()
                    flash(f"Data {submit} succeeded.", 'success')
                    return redirect(
                        url_for(
                            redirect_page,
                            table=table,
                            schema=schema,
                            subtable=subtable,
                            overwrite='True',
                            _id=str(_id)
                        )
                    )
            else:
                flash(f"Form appears incomplete; check error messages on "
                      "fields and in pop-ups of parent tables", 'warning')

        form.append_hidden_entries()

    elif _id is not None:
        # show enter fields
        enter_show = ['show', 'true']

        if (edit == 'True') or (overwrite == 'True'):
            readonly.extend(dynamicform.populate_form(
                _id, form, is_edit=edit,
                **kwargs
            ))

    return render_template(
        f'pages/{page}.html',
        form=form,
        data=data,
        table_name=table_name,
        url=url_for('table', table=table, schema=schema, subtable=subtable),
        toggle_off_keys=toggle_off_keys,
        filename=filename,
        enter_show=enter_show,
        readonly=readonly
    )
