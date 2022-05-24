from django.db import migrations, models


def split_classifications(apps, schema_editor):
    AIClassification = apps.get_model('a4_candy_classifications', 'AIClassification')

    classifications = AIClassification.objects.all()
    for classification in classifications:
        if len(classification.classifications) > 1:
            for category in classification.classifications:

                AIClassification.objects.create(
                    created=classification.created,
                    modified=classification.modified,
                    is_pending=classification.is_pending,
                    classifications=[category],
                    comment_text=classification.comment_text,
                    comment=classification.comment
                )

            classification.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_classifications', '0007_add_related_names'),
    ]

    operations = [
        migrations.RunPython(split_classifications),
        migrations.AlterField(
            model_name='aiclassification',
            name='classifications',
            field=models.CharField(
                choices=[('OFFENSIVE', 'offensive'), ('ENGAGING', 'engaging'), ('FACTCLAIMING', 'fact claiming'),
                         ('OTHER', 'other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='userclassification',
            name='classifications',
            field=models.CharField(
                choices=[('OFFENSIVE', 'offensive'), ('ENGAGING', 'engaging'), ('FACTCLAIMING', 'fact claiming'),
                         ('OTHER', 'other')], max_length=50),
        ),
        migrations.RenameField(
            model_name='aiclassification',
            old_name='classifications',
            new_name='classification',
        ),
        migrations.RenameField(
            model_name='userclassification',
            old_name='classifications',
            new_name='classification',
        ),
    ]

