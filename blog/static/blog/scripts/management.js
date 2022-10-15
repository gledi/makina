window.addEventListener("load", (ev) => {
  const postsTable = document.querySelector(".table-posts");

  postsTable.addEventListener("click", async (ev) => {
    const btn = ev.target;

    if (btn.tagName === "BUTTON") {
      console.log("target:", ev.target, ev.target.tagName);
      const postId = parseInt(btn.dataset["postid"], 10);

      const resp = await fetch("/posts/publish/", {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify({ postId: postId }),
      });

      if (resp.ok) {
        btn.disabled = true;
      } else {
        const alertsContainer = document.querySelector("#alerts");
        const alertElem = document.createElement("p");
        alertElem.innerText = "Could not publish post!";
        alertsContainer.appendChild(alertElem);
      }
    }
  });
});
