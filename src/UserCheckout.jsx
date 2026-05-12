import React, { useState } from 'react';
import { 
  Box, Card, CardContent, Typography, Button, Grid, IconButton, 
  Divider, Chip, Dialog, DialogTitle, DialogContent, DialogActions, Slide, Fade 
} from '@mui/material';
import { 
  ShoppingCart, Add, Remove, Delete, LocalOffer, AutoAwesome
} from '@mui/icons-material';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const MENU_ITEMS = [
  { id: 1, name: 'Laptop', price: 45000, category: 'Electronics & Tech' },
  { id: 2, name: 'Wireless Mouse', price: 1200, category: 'Accessories' },
  { id: 3, name: 'DSLR Camera', price: 55000, category: 'Electronics & Tech' },
  { id: 4, name: 'SD Card', price: 800, category: 'Accessories' },
  { id: 5, name: 'Pasta', price: 250, category: 'Food & Restaurant' },
  { id: 6, name: 'Garlic Bread', price: 100, category: 'Food & Restaurant' },
  { id: 7, name: 'Diapers', price: 600, category: 'Parents & Baby' },
  { id: 8, name: 'Wet Wipes', price: 150, category: 'Parents & Baby' },
  { id: 9, name: 'Notebooks (Set of 5)', price: 300, category: 'School & Education' },
  { id: 10, name: 'Blue Pens', price: 50, category: 'School & Education' },
];

export default function UserCheckout() {
  const [cart, setCart] = useState([]);
  const [showOffer, setShowOffer] = useState(false);
  const [currentOffer, setCurrentOffer] = useState(null);

  const handleAddToCart = (item) => {
    setCart(prev => {
      const existing = prev.find(i => i.id === item.id);
      if (existing) {
        return prev.map(i => i.id === item.id ? { ...i, qty: i.qty + 1 } : i);
      }
      return [...prev, { ...item, qty: 1 }];
    });

    // AI Logic Trigger Simulation
    const checkBundle = (trigger, offerName, discountText, discountPrice, message, lift) => {
      if (item.name === trigger && !cart.find(i => i.name === offerName)) {
        setCurrentOffer({
          triggerItem: trigger,
          offerItem: MENU_ITEMS.find(i => i.name === offerName),
          discountText,
          discountPrice,
          message,
          aiType: `Market Basket Analysis (Lift: ${lift})`
        });
        setTimeout(() => setShowOffer(true), 800);
        return true;
      }
      return false;
    };

    checkBundle('Laptop', 'Wireless Mouse', '30% OFF Mouse', 840, 'The Essentials Bundle: Customers who bought this laptop also bought a wireless mouse.', 3.5) ||
    checkBundle('DSLR Camera', 'SD Card', '50% OFF SD Card', 400, 'The Ready-to-Shoot Kit: Get an SD card at 50% off to start shooting immediately!', 4.2) ||
    checkBundle('Pasta', 'Garlic Bread', 'Free Garlic Bread', 0, 'The Italian Classic: High demand! Add Garlic bread for free to complete your meal.', 2.8) ||
    checkBundle('Diapers', 'Wet Wipes', '25% OFF Wipes', 112, 'The Hygiene Essential: Parents who buy diapers also need wet wipes. Add now to save!', 5.1) ||
    checkBundle('Notebooks (Set of 5)', 'Blue Pens', 'Flash Sale: ₹20', 20, 'The Semester Start: Grab some blue pens to go with your new notebooks.', 1.9);
  };

  const handleUpdateQty = (id, delta) => {
    setCart(prev => prev.map(item => {
      if (item.id === id) {
        const newQty = item.qty + delta;
        return newQty > 0 ? { ...item, qty: newQty } : item;
      }
      return item;
    }));
  };

  const handleRemove = (id) => {
    setCart(prev => prev.filter(item => item.id !== id));
  };

  const acceptOffer = () => {
    if (currentOffer.offerItem) {
      setCart(prev => [...prev, { ...currentOffer.offerItem, price: currentOffer.discountPrice, qty: 1, isOffer: true }]);
    } else {
      // Modify existing item price (e.g. Tomato Soup)
      setCart(prev => prev.map(i => i.name === currentOffer.triggerItem ? { ...i, price: currentOffer.discountPrice, isOffer: true } : i));
    }
    setShowOffer(false);
  };

  const cartTotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);

  return (
    <Box sx={{ p: 4, height: '100%', bgcolor: 'background.default' }}>
      <Typography variant="h4" fontWeight="bold" mb={1}>Self-Service Kiosk</Typography>
      <Typography variant="body2" color="text.secondary" mb={4}>Experience the AI from the customer's point of view.</Typography>

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Typography variant="h6" mb={2}>Menu</Typography>
          <Grid container spacing={2}>
            {MENU_ITEMS.map(item => (
              <Grid item xs={12} sm={6} key={item.id}>
                <Card sx={{ bgcolor: 'background.paper', border: '1px solid rgba(255,255,255,0.05)' }}>
                  <CardContent sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="h6">{item.name}</Typography>
                      <Typography color="text.secondary" variant="body2">{item.category}</Typography>
                      <Typography color="primary.main" fontWeight="bold" mt={1}>₹{item.price}</Typography>
                    </Box>
                    <IconButton color="primary" onClick={() => handleAddToCart(item)} sx={{ bgcolor: 'rgba(124, 58, 237, 0.1)' }}>
                      <Add />
                    </IconButton>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', border: '1px solid rgba(255,255,255,0.1)' }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Box display="flex" alignItems="center" gap={1} mb={3}>
                <ShoppingCart />
                <Typography variant="h6">Your Cart</Typography>
              </Box>

              {cart.length === 0 ? (
                <Typography color="text.secondary" textAlign="center" mt={4}>Cart is empty</Typography>
              ) : (
                <Box display="flex" flexDirection="column" gap={2}>
                  {cart.map(item => (
                    <Box key={item.id} display="flex" justifyContent="space-between" alignItems="center">
                      <Box flex={1}>
                        <Typography variant="body1" fontWeight="bold" display="flex" alignItems="center" gap={1}>
                          {item.name} 
                          {item.isOffer && <Chip size="small" icon={<LocalOffer fontSize="small"/>} label="Offer" color="secondary" sx={{ height: 20, fontSize: '10px' }}/>}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">₹{item.price} x {item.qty}</Typography>
                      </Box>
                      <Box display="flex" alignItems="center" gap={1}>
                        <IconButton size="small" onClick={() => handleUpdateQty(item.id, -1)} disabled={item.qty <= 1}><Remove fontSize="small" /></IconButton>
                        <Typography>{item.qty}</Typography>
                        <IconButton size="small" onClick={() => handleUpdateQty(item.id, 1)}><Add fontSize="small" /></IconButton>
                        <IconButton size="small" color="error" onClick={() => handleRemove(item.id)}><Delete fontSize="small" /></IconButton>
                      </Box>
                    </Box>
                  ))}
                </Box>
              )}
            </CardContent>
            <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)' }} />
            <Box p={3}>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="h6">Total</Typography>
                <Typography variant="h6" fontWeight="bold" color="primary.main">₹{cartTotal}</Typography>
              </Box>
              <Button variant="contained" color="primary" fullWidth size="large" disabled={cart.length === 0}>
                Checkout Now
              </Button>
            </Box>
          </Card>
        </Grid>
      </Grid>

      {/* AI Dynamic Offer Dialog */}
      <Dialog 
        open={showOffer} 
        TransitionComponent={Transition} 
        keepMounted 
        onClose={() => setShowOffer(false)}
        PaperProps={{ sx: { bgcolor: 'background.paper', backgroundImage: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.02))', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: 4 } }}
      >
        <DialogTitle sx={{ display: 'flex', alignItems: 'center', gap: 1, color: 'success.light' }}>
          <AutoAwesome /> Smart Offer Unlocked!
        </DialogTitle>
        <DialogContent>
          <Typography variant="body1" mb={2}>{currentOffer?.message}</Typography>
          {currentOffer?.offerItem && (
            <Card sx={{ bgcolor: 'rgba(0,0,0,0.2)', border: '1px dashed rgba(255,255,255,0.2)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', p: 2 }}>
              <Box>
                <Typography fontWeight="bold">{currentOffer.offerItem.name}</Typography>
                <Typography variant="caption" sx={{ textDecoration: 'line-through', color: 'text.secondary', mr: 1 }}>₹{currentOffer.offerItem.price}</Typography>
                <Typography variant="body2" color="secondary.main" display="inline">₹{currentOffer.discountPrice}</Typography>
              </Box>
              <Chip label={currentOffer.discountText} color="secondary" />
            </Card>
          )}
          {!currentOffer?.offerItem && (
             <Chip label={currentOffer?.discountText} color="secondary" sx={{ mt: 1 }} />
          )}
          <Box mt={3} p={1.5} bgcolor="rgba(255,255,255,0.05)" borderRadius={2}>
            <Typography variant="caption" color="text.secondary" display="flex" alignItems="center" gap={1}>
              <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: 'primary.main' }} />
              AI Logic Triggered: {currentOffer?.aiType}
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 3, pt: 0 }}>
          <Button onClick={() => setShowOffer(false)} color="inherit">No Thanks</Button>
          <Button onClick={acceptOffer} variant="contained" color="secondary" sx={{ color: '#000', fontWeight: 'bold' }}>
            Accept Offer
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
