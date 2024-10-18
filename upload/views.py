from django.shortcuts import render
from django.core.mail import send_mail
import pandas as pd
from .forms import UploadFileForm

def handle_uploaded_file(f):
    # Read the uploaded file (Excel or CSV)
    if f.name.endswith('.xlsx'):
        df = pd.read_excel(f)
    else:
        df = pd.read_csv(f)

    # Generate the summary report using pandas
    summary = df.describe(include='all').to_string()
    return summary

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the uploaded file and generate the summary
            summary = handle_uploaded_file(request.FILES['file'])

            # Send the email with the summary
            send_mail(
                subject="Python Assignment - Aniket Khomane",
                message=summary,
                from_email='your-email@example.com',  # Replace with your email
                recipient_list=['tech@themedius.ai'],
            )

            # Render the success page with the summary report
            return render(request, 'upload/success.html', {'summary': summary})
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})
