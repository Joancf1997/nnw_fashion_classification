<template>
  <div class="todo">
    <div id="title"> Clothes Classifier  </div>
    <div id="wrapper">
      <div class="actionsSpace"> 
        <button id="clearbtn" @click="clearCanvas()"> Clear </button>
        <button v-if="!imageSrc" id="classifybtn" @click="sendImage()"> Classify Drawing </button>
        <button v-if="imageSrc" id="classifybtn" @click="uploadFile()"> Classify Image </button>
        <div id="loadbtn"> 
          <input type="file" @change="onFileSelected" />
        </div>
      </div>
      <div v-show="imageSrc" class="canvasSpace">
        <img  class="image" :src="imageSrc" alt="Selected Image" style="max-width: 560px; height: 560px;" />
      </div>
      <div v-show="!imageSrc" class="canvasSpace"> 
        <canvas ref="canvas" width="560px" height="560px" class="canvas"></canvas>
      </div>
      <div class="PredictionLabel"> {{ prediction }} - {{ confidence }}  </div>
    </div>
  </div>
</template>

<style scoped>

.todo{
  width: 65vw;
}

#title{ 
  width: 100%;
  height: 100px;
  font-weight: bold;
  font-size: 4em;
  margin-top: 100px;
  text-align: center;
}

.image{  
  display: inline;
}

.canvas{  
  display: inline;
  border:1px solid #000;
}

#wrapper{ 
  width: 100%;
  height: 650px;
}

.canvasSpace{ 
  width: 100%;
  text-align:center;
  float: left;
  width: 100%;
}

.actionsSpace{ 
  float: left;
  width: 100%;
  height: 70px;
  margin-top: 30px;
  margin-bottom: 30px;
}

#clearbtn{ 
  width: 30%;
  float: left;
  border: 2px solid rgba(255, 1, 1, 0.593);
  color: red;
  background-color: transparent;
  height: 100%;
  border-radius: 20px;
  font-size: 2em;
  font-weight: 300;

}

#classifybtn{ 
  width: 30%;
  float: left;
  border: 2px solid rgba(19, 145, 3, 0.593);
  color: green;
  background-color: transparent;
  height: 100%;
  border-radius: 20px;
  font-size: 2em;
  font-weight: 300;
  margin-left: 5%;
}

#loadbtn{ 
  width: 30%;
  float: left;
  border: 2px solid rgba(1, 65, 255, 0.593);
  color: blue;
  background-color: transparent;
  height: 100%;
  border-radius: 20px;
  font-size: 2em;
  font-weight: 300;
  margin-left: 5%;
}

.PredictionLabel{ 
  float:left;
  width: 100%;
  font-size: 2em;
  text-align: center;
  margin-top: 20px;
}
</style>



<script setup>
import api from "@/boot/axios"
import { ref, onMounted, onUnmounted } from 'vue';

const canvas = ref(null);
const pensilDown = ref(false);
const prediction = ref("")
const confidence = ref("")
const selectedFile = ref(null)
const imageSrc = ref(null)


const onFileSelected = (event) => {
  selectedFile.value = event.target.files[0];
  if (selectedFile.value) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imageSrc.value = e.target.result; // Store the base64 image string
    };
    reader.readAsDataURL(selectedFile.value);
  }
}

const uploadFile = async () => {
  if (!selectedFile.value) {
    alert('Please select a file first!');
    return;
  }

  const formData = new FormData();
  formData.append('file', selectedFile.value);

  api.post('/predictions', formData) 
  .then((response) => {
  if(response.status == 200) { 
    prediction.value = response.data.prediction
    confidence.value = `${response.data.confidence} %`
  }
  })
  .catch((error) => {
    console.log(error)
  })
}

const draw = (event) => {
  if(pensilDown.value){ 
    const rect = canvas.value.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
  
    const ctx = canvas.value.getContext('2d');
    ctx.fillStyle = 'black';
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, Math.PI * 2);
    ctx.fill();
  }
};

const sendImage = async () => {
  const canvas = document.querySelector('canvas'); 
  // Convert the canvas to a Blob
  canvas.toBlob(async (blob) => {
    // Create a FormData object
    const formData = new FormData();
    formData.append('file', blob, 'drawing.png');

    api.post('/predictions', formData) 
    .then((response) => {
    if(response.status == 200) { 
      prediction.value = response.data.prediction
      confidence.value = `${response.data.confidence} %`
    }
    })
    .catch((error) => {
      console.log(error)
    })
  }, 'image/png'); // Convert canvas to Blob in PNG format
};

const clearCanvas = () => { 
    
  prediction. value = ""
  confidence.value = ""
  imageSrc.value = null
  selectedFile.value = null
  const ctx = canvas.value.getContext('2d');
  ctx.clearRect(0, 0, 560, 560);
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, 560, 560);
}

const mouseDown = () => { 
  pensilDown.value = true
}

const mouseUp = () => { 
  pensilDown.value = false
}

onMounted(() => {
  canvas.value.addEventListener('mousemove', draw);
  canvas.value.addEventListener('touchmove', draw);
  canvas.value.addEventListener('mousedown', mouseDown);
  canvas.value.addEventListener('mouseup', mouseUp);
// is better with black filled imaged
  const rect = canvas.value.getBoundingClientRect();
  const ctx = canvas.value.getContext('2d');
  ctx.clearRect(0, 0, 560, 560);
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, 560, 560);
});

onUnmounted(() => {
  canvas.value.removeEventListener('mousemove', draw);
  canvas.value.removeEventListener('touchmove', draw);
  canvas.value.removeEventListener('mousedown', mouseDown);
  canvas.value.removeEventListener('mouseup', mouseUp);
});

</script>
