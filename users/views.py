from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class PaymentsListAPIView(generics.ListAPIView):
    """Payments list endpoint"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course_paid', 'lesson_paid', 'payment_method',)
    ordering_fields = ('date_payment',)


class UserCreateAPIView(generics.CreateAPIView):
    """User create endpoint"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsCreateAPIView(generics.CreateAPIView):
    """Payment create endpoint"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, payment_method='безналичный расчет')
        product = create_stripe_product(payment.course_paid.name)
        price = create_stripe_price(product=product, amount=payment.payment_amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()
