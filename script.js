function changeImage() {
  var image = document.getElementById("image");
  var buttonText = document.getElementById("buttonText");
  
  var metaImage = document.querySelector('meta[property="fc:frame:input:image"]');
  var metaButton = document.querySelector('meta[property="fc:frame:button:1"]');
  var metaButton2 = document.querySelector('meta[property="fc:frame:button:2"]');
  
  if (buttonText.innerText === "Join Here") {
    image.src = metaImage.getAttribute("content");
    buttonText.innerText = metaButton2.getAttribute("content");
  } else {
    image.src = "https://henpedia.my.id/image3.jpg"; // URL gambar kedua
    buttonText.innerText = metaButton.getAttribute("content");
  }
}