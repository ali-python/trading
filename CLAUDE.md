# CLAUDE.md — Trading / Inventory System

> This file is for Claude Code. It contains full project context, known bugs, and working instructions.

---

## Project Overview

**Name:** Partum Trading — Inventory Management System
**Framework:** Django 2.2.6
**Python:** 3.12
**Database:** SQLite3 (`db.sqlite3`)
**Timezone:** Asia/Karachi

---

## Project Structure

```
trading/
├── partum_trading/        # Main Django project (settings, urls, wsgi)
├── common/                # Login mixin, context processor, shared views
├── product/               # Products, purchased items, karigar products
├── customer/              # Customer management
├── sales/                 # Sales records
├── expense/               # Expense tracking
├── banking_system/        # Bank accounts / transactions
├── supplier/              # ⚠️  Supplier & SupplierStatement (BUGS ARE HERE)
├── templates/             # HTML templates (app-wise subfolders)
├── app_static/            # Static files (CSS, JS)
├── requirements.txt
└── manage.py
```

---

## Apps and URL Prefixes

| App             | URL Prefix      | Namespace     |
|-----------------|-----------------|---------------|
| common          | `/`             | `common`      |
| product         | `/product/`     | `product`     |
| customer        | `/customer/`    | `customer`    |
| expense         | `/expense/`     | `expense`     |
| sales           | `/sales/`       | `sales`       |
| banking_system  | `/bank_detail/` | `bank`        |
| supplier        | `/supplier/`    | `supplier`    |

---

## Supplier App — Bugs and Issues

### 🔴 BUG 1: Wrong `.get()` call in `supplier_remaining_amount()` method

**File:** `supplier/models.py`
**Method:** `Supplier.supplier_remaining_amount()`

```python
# ❌ BROKEN CODE (current)
total_amount = supplier_statement.aggregate(Sum('supplier_amount'))
total_amount = supplier_statement.get('supplier_amount__sum') or 0  # BUG!
```

**Problem:** `.aggregate()` returns a dictionary, but `.get()` is being called on the QuerySet — this raises a `TypeError` at runtime.

```python
# ✅ FIXED CODE
def supplier_remaining_amount(self):
    data = self.supplier.all().aggregate(
        total_amount=Sum('supplier_amount'),
        total_payments=Sum('payment_amount')
    )
    total_amount = data['total_amount'] or 0
    total_payments = data['total_payments'] or 0
    return total_amount - total_payments
```

---

### 🔴 BUG 2: Wrong ORM query in `SupplierStatementUpdate` view

**File:** `supplier/views.py`
**Class:** `SupplierStatementUpdate.get_context_data()`

```python
# ❌ BROKEN CODE (current)
supplier = Supplier.objects.get(supplier__id=self.kwargs.get('pk'))
# 'supplier' here is the related_name of SupplierStatement, not a Supplier field
# This raises DoesNotExist or FieldError
```

**Problem:** `pk` here is the `SupplierStatement` ID, but the code tries to look up a `Supplier` using the wrong field.

```python
# ✅ FIXED CODE
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    statement = self.get_object()
    context['supplier'] = statement.supplier
    return context
```

---

### 🟡 BUG 3: `supplier` field exposed in `SupplierStatementFormView`

**File:** `supplier/forms.py`

```python
# ❌ CURRENT CODE (problematic)
class SupplierStatementFormView(forms.ModelForm):
    class Meta:
        model = SupplierStatement
        fields = '__all__'  # exposes the supplier dropdown to users
```

**Problem:** `fields = '__all__'` includes the `supplier` field in the form, letting users select any supplier. The supplier should be set from the URL, not from the form.

```python
# ✅ FIXED CODE
class SupplierStatementFormView(forms.ModelForm):
    class Meta:
        model = SupplierStatement
        fields = ['supplier_amount', 'payment_amount', 'description', 'date']
```

---

### 🟡 BUG 4: Confusing `related_name='supplier'`

**File:** `supplier/models.py`

```python
# ❌ CONFUSING (current)
supplier = models.ForeignKey(Supplier, ..., related_name='supplier')
```

**Problem:** The field name and `related_name` are both `supplier` — causes ORM confusion and IDE ambiguity.

```python
# ✅ FIXED CODE
supplier = models.ForeignKey(Supplier, ..., related_name='statements')
# Then run:
# python manage.py makemigrations supplier
# python manage.py migrate
```

> ⚠️ After this change, update `supplier_remaining_amount()` to use `self.statements.all()`.

---

### 🟡 BUG 5: Duplicate authentication check in `StatementPayment`

**File:** `supplier/views.py`

```python
# ❌ REDUNDANT (current)
class StatementPayment(CustomLoginRequiredMixin, FormView):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:  # already handled by mixin
            return HttpResponseRedirect(reverse('login'))
        return super(...)
```

**Fix:** Delete the entire `dispatch` method — `CustomLoginRequiredMixin` already handles it.

---

### 🟡 BUG 6: NULL allowed with CASCADE on `SupplierStatement.supplier`

**File:** `supplier/models.py`

```python
# ❌ INCONSISTENT (current)
supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
```

**Fix:** If a statement must always belong to a supplier, remove `null=True, blank=True`:

```python
# ✅ FIXED CODE
supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='statements')
```

---

## Project-Wide Issues

### 🔴 SECRET_KEY is hardcoded in settings.py

```python
# ❌ CURRENT
SECRET_KEY = 'wbdel!sah+=(qh_m$^m4vv%fu&8+pq-%xaped7fjfl3nfuus&_'

# ✅ FIXED
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-only-for-dev')
```

### 🟡 Django version is end-of-life

`Django==2.2.6` — upgrade to Django 4.2 LTS or 5.x.

### 🟡 `ALLOWED_HOSTS = []` is unsafe for production

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

---

## Development Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Start server
python manage.py runserver
```

---

## Common Commands

```bash
python manage.py makemigrations supplier
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
python manage.py collectstatic
```

---

## Supplier App — URL Reference

| URL Pattern | View | Name |
|---|---|---|
| `/supplier/add/` | `SupplierAdd` | `supplier:add_supplier` |
| `/supplier/lists/` | `SupplierList` | `supplier:list_supplier` |
| `/supplier/supplier/statements/list/<pk>/` | `SupplierStatementList` | `supplier:list_supplier_statement` |
| `/supplier/statement/payment/<pk>/` | `StatementPayment` | `supplier:payment` |
| `/supplier/supplier/add/statements/<pk>/` | `AddSupplierStatement` | `supplier:add_supplier_statement` |
| `/supplier/update/statements/<pk>/` | `SupplierStatementUpdate` | `supplier:update_supplier_statement` |
| `/supplier/delete/<pk>/` | `SupplierDelete` | `supplier:supplier_confirm_delete` |

---

## Priority Fix Order (for Claude Code)

1. **🔴 Fix first:** `supplier_remaining_amount()` — wrong `.get()` call crashes at runtime
2. **🔴 Fix next:** `SupplierStatementUpdate.get_context_data()` — wrong ORM query raises an error
3. **🟡 Then:** Rename `related_name='supplier'` to `'statements'` + run migration
4. **🟡 Then:** Remove `fields = '__all__'` from `SupplierStatementFormView`
5. **🟡 Then:** Remove duplicate `dispatch` method from `StatementPayment`
6. **🟡 Then:** Move `SECRET_KEY` to an environment variable