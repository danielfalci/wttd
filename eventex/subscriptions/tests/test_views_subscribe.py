# coding: utf-8
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')
       
    def test_get(self):
        'GET /inscricao/ must return status code 200.'
        self.assertEqual(200, self.resp.status_code)
    
    def test_template(self):
        'Response should be a rendered template.'
        self.assertTemplateUsed(self.resp, 
                                'subscriptions/subscription_form.html')
                                
    def test_html(self):
        'HTML must contain input controls.'
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')
        
    def test_csrf(self):
        'HTML must contain crsf token.'
        self.assertContains(self.resp, 'csrfmiddlewaretoken')
        
    def test_has_form(self):
        'Context must have the subscription form.'
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)
        
class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='12345678901',
                    email='outro@email.com', phone='21-96186180')
        self.resp = self.client.post('/inscricao/', data)
        
    def test_post(self):
        'Valid POST should redirect to /inscricao/1/'
        self.assertEqual(302, self.resp.status_code)
        
    def test_save(self):
        'Valid POST must be saved.'
        self.assertTrue(Subscription.objects.exists())
        
class SubscribeInvalidPostTest(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='000000000012',
                    email='henrique@bastos.net', phone='21-96186180')
        self.resp = self.client.post('/inscricao/', data)
        
    def test_post(self):
        'Invalid POST should not redirect.'
        self.assertEqual(200, self.resp.status_code)
        
    def test_form_errors(self):
        'Form must containt errors.'
        self.assertTrue(self.resp.context['form'].errors)
        
    def test_dont_save(self):
        'Do not save data.'
        self.assertFalse(Subscription.objects.exists())