from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse

from contact.models import Contact
from contact.forms import ContactForm


def create(request):
    form_action = reverse('contact:create')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context
        )

    # SE O MÉTODO DE REQUISIÇÃO NÃO FOR POST...
    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }
    
    return render(
        request,
        'contact/create.html',
        context
    )


def update(request, contact_id):
    contact = get_object_or_404(
        Contact,
        pk=contact_id,
        show=True
    )
    # contact_id -----> recebemos dinamicamente do form no html                         
    form_action = reverse('contact:update', args=(contact_id), )

    if request.method == 'POST':
        # instance = Model do banco de dados, para assim, após a requisição POST, também atualizar os dados no BD.
        form = ContactForm(request.POST, instance=contact)

        context = {
            'form': form,
            'form_action': form_action,
        }
    
        if form.is_valid():
            contact = form.save()
            # Aqui eu redireciono para a url name UPDATE
            # E meio que dou um POST, para atualizar aquele devido contato, com base no ID, recebido no inicio da view.
            return redirect('contact:update', contact_id=contact.pk)
        
        return render(
            request,
            'contact/create.html',
            context
        )
    
    # Aqui seria o ELSE do primeiro IF, então basicamente
    # Se o request.method não for POST, caimos aqui.
    # Onde só limpamos o formulário mesmo (eu imagino)
    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )