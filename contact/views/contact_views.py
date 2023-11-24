from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q  # Possibilita fazer o uso de PIPE no filter() quando se usa icontains por ex...
from contact.models import Contact

# view -------------------- INDEX
def index(request):
               # Para trazer todos os contatos da base de dados (Model - Contact).
               # Estamos utilizando também, um fitro/query para essa busca no Model.
    contacts = Contact.objects.all().filter(show=True).order_by('-id')[:5]

    context = {
        'contacts': contacts,
        'site_title': 'Contatos - '
    }

    return render(
        request,
        'contact/index.html',
        context
    )
# view -------------------- INDEX

# view -------------------- CONTACT
def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    single_contact = get_object_or_404(
        Contact, pk=contact_id, show=True
    )
    site_title = f'{single_contact.first_name} {single_contact.last_name} - '

    context = {
        'contact': single_contact,
        'site_title': site_title
    }

    return render(
        request,
        'contact/contact.html',
        context
    )
# view -------------------- CONTACT

def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('contact:index')
        
    contacts = Contact.objects \
               .filter(show=True) \
               .filter(
                   Q(first_name__icontains=search_value) |
                   Q(last_name__icontains=search_value) |
                   Q(phone__icontains=search_value) |
                   Q(email__icontains=search_value)
               ) \
               .order_by('-id')
    
    context = {
        'contacts': contacts,
        'site_title': 'Search - '
    }

    return render(
        request,
        'contact/index.html',
        context
    )