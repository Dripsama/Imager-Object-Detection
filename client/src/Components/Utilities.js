export const drawRect = (detections, ctx) => {
    detections.forEach((prediction) => {
      const [x, y, width, height] = prediction["bbox"];
      const text = prediction["class"];
  
      //Styling
      // const color = Math.floor(Math.random() * 16777215).toString(16);
      ctx.strokeStyle = "#FFFF00";
      ctx.font = "20px Arial";
  
      // Draw rectangles and text
      ctx.beginPath();
      ctx.fillStyle = "#FFFF00";
      ctx.fillText(text, x, y);
      ctx.rect(x, y, width, height);
      ctx.stroke();
    });
  };
  