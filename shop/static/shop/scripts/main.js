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

      const resp = await fetch(`${checkoutSessionUrl}?productId=${productId}`);
      const data = await resp.json();
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    }
  });
});


