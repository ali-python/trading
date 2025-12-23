from django.urls import path
from supplier.views import ( SupplierList,SupplierStatementList,SupplierAdd,AddSupplierStatement,SupplierStatementUpdate,StatementPayment,SupplierDelete )
app_name = 'supplier' 
urlpatterns = [
    path('add/', SupplierAdd.as_view(), name='add_supplier'),
    path('lists/', SupplierList.as_view(), name='list_supplier'),
    path('supplier/statements/list/<int:pk>/', SupplierStatementList.as_view(), name='list_supplier_statement'),
    path('statement/payment/<int:pk>/',StatementPayment.as_view(),name='payment'),
    path('supplier/add/statements/<int:pk>/', AddSupplierStatement.as_view(), name='add_supplier_statement'),
    path('update/statements/<int:pk>/',SupplierStatementUpdate.as_view(),name='update_supplier_statement'),
    path('delete/<int:pk>/', SupplierDelete.as_view(), name="supplier_confirm_delete")
]