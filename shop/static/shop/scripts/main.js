window.addEventListener("load", async ev => {
  const resp = await fetch(configUrl);
  const data = await resp.json();
  console.log("PUBLIC KEY =", data.publicKey);

  const stripe = Stripe(data.publicKey);

  const productListContainer = document.querySelector("#product-list");

  productListContainer.addEventListener("click", async e => {
    const nodeName = e.target.nodeName;
    let elem = e.target;
    if (elem.classList.contains("purchase")) {
      if (nodeName === "I" || nodeName === "SPAN") {
        elem = elem.closest("button");
      }

      const priceId = elem.dataset.price;
      const productId = elem.dataset.product;
      const quantity = 1;

      const resp = await fetch(addToCartUrl, {
        method: 'POST',
        body: JSON.stringify({product_id: productId, quantity: quantity}),
        headers: {
          'Content-Type': 'application/json'
        }
      });
      const data = await resp.json();

      const itemsCountElem = document.querySelector("#cart-items-count");
      itemsCountElem.innerText = data.total_items;


      // const resp = await fetch(`${checkoutSessionUrl}?productId=${productId}`);
      // const data = await resp.json();
      // return stripe.redirectToCheckout({sessionId: data.sessionId});
    }
  });
});


