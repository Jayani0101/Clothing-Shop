from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='final_total',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=50, default="Not Selected"),
        ),
         migrations.AddField(
	    model_name='orderitem',
	    name='price',
	    field=models.DecimalField(max_digits=10, decimal_places=2, default=0),
	),

    ]

