# Stripe Payments — No Fees on First $1000

## When to Use
- SaaS billing
- Ecommerce
- Any payment integration

## Quick Setup
```bash
# Claim at: https://stripe.com/education
# Get test keys from: https://dashboard.stripe.com/test/apikeys

# Save keys
echo "STRIPE_SECRET_KEY=sk_test_xxx" >> ~/.config/global-apikeys/keys.env
echo "STRIPE_PUBLISHABLE_KEY=pk_test_xxx" >> ~/.config/global-apikeys/keys.env
```

## Node.js — Checkout Session
```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

app.post('/create-checkout', async (req, res) => {
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{ price: 'price_xxx', quantity: 1 }],
    mode: 'payment',
    success_url: 'https://yoursite.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url: 'https://yoursite.com/cancel',
  });
  res.json({ sessionId: session.id });
});
```

## Python — Checkout Session
```python
import stripe
stripe.api_key = os.environ['STRIPE_SECRET_KEY']

@app.post("/create-checkout")
async def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": "price_xxx", "quantity": 1}],
        mode="payment",
        success_url="https://yoursite.com/success",
        cancel_url="https://yoursite.com/cancel",
    )
    return {"sessionId": session.id}
```

## Subscriptions
```javascript
// Create subscription
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  line_items: [{ price: 'price_monthly_xxx', quantity: 1 }],
  success_url: 'https://yoursite.com/success',
  cancel_url: 'https://yoursite.com/cancel',
});

// Webhook for subscription events
app.post('/webhooks/stripe', express.raw({type: 'application/json'}), (req, res) => {
  const sig = req.headers['stripe-signature'];
  const event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  
  switch (event.type) {
    case 'invoice.paid':
      // Grant access
      break;
    case 'invoice.payment_failed':
      // Revoke access, notify user
      break;
  }
  res.json({received: true});
});
```

## Customer Portal
```javascript
// Let users manage subscriptions
const session = await stripe.billingPortal.sessions.create({
  customer: 'cus_xxx',
  return_url: 'https://yoursite.com/account',
});
```

## Webhook Events to Handle
| Event | Action |
|-------|--------|
| `checkout.session.completed` | Grant access |
| `invoice.paid` | Extend subscription |
| `invoice.payment_failed` | Revoke access, notify |
| `customer.subscription.deleted` | Revoke access |
| `charge.refunded` | Revoke access |

## Student Benefits
- No transaction fees on first $1000 revenue
- Full API access
- Dashboard + analytics
- Webhook support
