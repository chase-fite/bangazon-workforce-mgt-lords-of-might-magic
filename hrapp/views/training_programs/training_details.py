import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from hrapp.models import TrainingProgram
from ..connection import Connection



def get_training(training_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            *
        from hrapp_trainingprogram ht
        WHERE ht.id = ?
        """, (training_id,))

        return db_cursor.fetchone()


def training_details(request, training_id):
    if request.method == 'GET':
        training = get_training(training_id)

        template = 'training_programs/training_details.html'
        context = {
            'training': training
        }

        return render(request, template, context)

    if request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
         ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_trainingprogram
                WHERE id = ?
                """, (training_id,))

        return redirect(reverse('hrapp:training_list'))