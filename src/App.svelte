<script>
  import { onMount } from "svelte";
  import * as d3 from "d3"
  import albums from "/src/data/albums_copy.csv"

  let streams = []; // Lista de streams ordenada como aparecen en el csv
  let anios = []; // Lista de años
  let anios_str = []; // Lista de años en formato string

  for (let i = 0; i < albums.length; i++) {
    streams.push(parseInt(albums[i].Streams));
  }

  for (let i = 0; i < 21; i++){
    anios.push(2003+i);
    anios_str.push((2003+i).toString());
  }

  function streams_str(numero) {
    return numero.toLocaleString("es-ES");
  }

  // Diccionario de colores para cada género
  const color_genero = {
    "Hip Hop/Rap": ["195",	"45",	"107", "0.75"],
    "Pop": ["210",	"111",	"235", "0.75"],
    "Rock": ["210",	"88",	"11", "0.75"],
    "R&B/Soul": ["1",	"151",	"246", "0.75"],
    "Latin/Regueton": ["252",	"186",	"4", "0.75"],
    "Otros": ["95",	"205",	"138", "0.75"],
  }

  // Escala para el tamaño de las burbujas
  let bubble_size = d3
    .scaleRadial()
    .domain([d3.min(streams), d3.max(streams)])
    .range([85, 200])

  //Función para devolver los 5 albums de un año
  function albums_of(anio){
    const begin = (anio - 2003)*5;
    const end = begin + 5;
    const rta = albums.slice(begin, end);
    return rta;
  }

  //Función para devolver una lista de los géneros de un album
  function genres(generos){
    const rta = generos.split(";");
    return rta;
  }

  //Función para devolver los géneros de un album en formato string
  function generos_str(generos){
    const generos_list = generos.split(";");
    let rta = "";
    for (let i = 0; i < generos_list.length-1; i++){
      rta += generos_list[i];
      rta += ", ";
    }
    rta += generos_list[generos_list.length-1];
    return rta;
  }

  //Función para asignar posiciones "aleatorias" a las burbujas principales
  //Las genera eligiendo de 5 posibles distribuciones predefinidas y agregandoles una pequeña variación aleatoria
  function generarPosiciones(anio) {
    let rv = [];
    const ancho = window.innerWidth;
    const alto = window.innerHeight;
    const curr_albums = albums_of(anio);
    let sizes = [];
    for (let i = 0; i < 5; i++) {
      sizes.push(bubble_size(parseInt(curr_albums[i].Streams)));
    }
    // Definimos posiciones iniciales para las burbujas principales
    const grids = [[[ancho*0.1,alto*0.15], [ancho*0.75,alto*0.10], [ancho*0.45,alto*0.35], [ancho*0.25,alto*0.60], [ancho*0.6,alto*0.65]],
                    [[ancho*0.1,alto*0.65], [ancho*0.65,alto*0.60], [ancho*0.45,alto*0.35], [ancho*0.25,alto*0.15], [ancho*0.7,alto*0.1]],
                    [[ancho*0.1,alto*0.1], [ancho*0.75,alto*0.35], [ancho*0.45,alto*0.15], [ancho*0.25,alto*0.55], [ancho*0.5,alto*0.65]],
                    [[ancho*0.25,alto*0.2], [ancho*0.60,alto*0.10], [ancho*0.1,alto*0.45], [ancho*0.45,alto*0.65], [ancho*0.8,alto*0.50]],
                    [[ancho*0.1,alto*0.7], [ancho*0.25,alto*0.20], [ancho*0.45,alto*0.35], [ancho*0.65,alto*0.65], [ancho*0.75,alto*0.1]]]
    const grid = grids[d3.randomInt(0,5)(1)];
    for (var i = 0; i < 5; i++) {
      //Modificamos la posición levemente de forma aleatoria
      let x = d3.randomUniform(-25,25)() + grid[i][0]; 
      let y = d3.randomUniform(-25,25)() + grid[i][1];
      // Si la burbuja se sale de la pantalla por abajo, la movemos hacia arriba
      while (y + sizes[i] + 120 > alto){
        y -= 25;
      }
      rv.push([x, y]);
    }
    return rv;
  }

  //Función para determinar si una burbuja de relleno se está superponiendo con una principal
  function isOverlapping(newBubble, main_bubbles) {
    const A = newBubble.x;
    const B = newBubble.y;
    const C = newBubble.x + newBubble.radius * 2;
    const D = newBubble.y + newBubble.radius * 2; 
    return main_bubbles.some(mainBubble => {
      const rect = mainBubble.getBoundingClientRect();
      const rect_text = mainBubble.querySelector("p").getBoundingClientRect();
      const a = rect.left-50;
      const b = (rect.top % window.innerHeight)-50;
      const c = a + rect.width+100;
      const d = b + rect.height+rect_text.height+100; 

      const superopone = (
        (a<A && A<c && b<B && B<d) ||
        (a<A && A<c && b<D && D<d) ||
        (a<C && C<c && b<B && B<d) ||
        (a<C && C<c && b<D && D<d)
      );

      return superopone;
    });
  }

  //Función para generar burbujas de relleno
  //Asigna un tamaño y posición aleatoria a cada burbuja. Intenta asignar posición hasta que no se superponga con una burbuja principal
  function generateFillBubbles(main_bubbles) {
    const fillBubbles = [];
    const numFillBubbles = parseInt(d3.randomUniform(50,70)(1)); // Número aleatorio de burbujas de relleno
    for (let i = 0; i < numFillBubbles; i++) {
      const radius = parseInt(d3.randomUniform(10,40)(1)); // Tamaño aleatorio
      //Asignar posicion en x y en y aleatoria
      const x = d3.randomUniform(-50, window.innerWidth-50)(1);
      const y = d3.randomUniform(-50, window.innerHeight)(1);
      const newBubble = {"x": x, "y": y, "radius": radius};
      // Si no hay superposición con una de las principales, agregamos la burbuja
      if (!isOverlapping(newBubble, main_bubbles)) {
        fillBubbles.push(newBubble);
      } else {
        i--; // Si hay superposición, intenta nuevamente
      }
    }
    return fillBubbles;
  }

  //Función para posicionar los círculos de colores en una burbuja principal
  function posicion_circulos(n) {
    const vertices = [];
    const r = 25;
    // Caso n = 1
    if (n === 1) {
      return [[0, 0]]; // Única posición en el centro
    }
    for (let k = 0; k < n; k++) {
      const theta = ((2 * Math.PI * k) / n) + Math.PI/2;
      const pos = [r * Math.cos(theta), r * Math.sin(theta)];
      vertices.push(pos);
    }
    return vertices;
  }

  //Función para determinar la imagen de la valoración
  function recuadro_valoracion(valoracion){
    if (valoracion == 1){
      return "/images/circle.png";
    }
    if (valoracion == 2){
      return "/images/dashed_circle.png";
    }
    if (valoracion == 4){
      return "/images/picos_circle.png";
    }
  }
  
  // Generar las posiciones de las burbujas principales para cada año
  let posiciones = [];
  for (let i = 0; i < 21; i++) {
    posiciones.push(generarPosiciones(2003+i));
  }

  //Devuelve un listado con las posiciones de las burbujas de un año
  function posiciones_for(anio){
    return posiciones[anio-2003];
  }

  //Observador para manejar la intersección de una página con el viewport y poder hacerla visible al scrollear
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
      } else {
        entry.target.classList.remove("show");
      }
    });
  },
  {
    threshold: 0.5
  }
  );

  //Función para manejar el scroll de la página
  const handleWheel = (event) => {
    if (!isScrolling) {
      isScrolling = true;
      container.removeEventListener('wheel', handleWheel);
      if (event.deltaY > 0) {
        // Scroll hacia abajo
        container.scrollBy({
          top: window.innerHeight, // Desplazarse hacia abajo una página
          behavior: 'smooth'
        });
      } else {
        // Scroll hacia arriba
        container.scrollBy({
          top: -window.innerHeight, // Desplazarse hacia arriba una página
          behavior: 'smooth'
        });
      }
      // Restablecer el estado después de un tiempo
      setTimeout(() => {
        isScrolling = false;
        container.addEventListener('wheel', handleWheel);
      }, 0); // Ajusta el tiempo según sea necesario
    }
    event.preventDefault(); // Prevenir el comportamiento predeterminado
  };

  let fill_bubbles = [];
  //Esperar al evento DOMContentLoaded (todo el contenido de la pagina cargado) para ejecutar el código
  document.addEventListener('DOMContentLoaded', () => {
    // Agregar el observador de intersección a cada página
    const targets = document.querySelectorAll(".page");
    targets.forEach((el) => {
      observer.observe(el);
    });
    
    const container = document.querySelector('.container');
    var isScrolling = false;

    // Agregar las burbujas de relleno a cada página
    const paginas = document.querySelectorAll('.vis');
    for (let i = 0; i < paginas.length; i++) {
      //Crear un div para las burbujas de relleno y agregarle su clase
      const filling = document.createElement('div');
      filling.className = 'filling';
      let mainBubbles = Array.from(paginas[i].querySelectorAll(".album_container")); //Tomar listado de las burbujas principales
      fill_bubbles = generateFillBubbles(mainBubbles); //Generar burbujas de relleno
      //Para cada burbuja de relleno, crear un div y agregarle su clase, posición, tamaño etc. y agregarlo al div de relleno
      fill_bubbles.forEach(bubble => {
        const bubbleElement = document.createElement('div');
        bubbleElement.className = 'bubble_filler';
        bubbleElement.style.left = `${bubble.x}px`;
        bubbleElement.style.top = `${bubble.y}px`;
        bubbleElement.style.position = 'relative';
        bubbleElement.style.animationDelay = `${Math.random() * 3}s`;
        bubbleElement.style.animationDuration = `${4 + Math.random() * 2}s`;
        bubbleElement.style.zIndex = -1;
        bubbleElement.style.opacity = d3.min([1, d3.randomUniform(0.1,0.5)(1)+bubble.radius/100]);
        const imagen = document.createElement('img');
        imagen.src = 'images/burbuja.png';
        imagen.alt = 'Bubble';
        imagen.style.position = 'absolute';
        imagen.style.maxWidth = `${bubble.radius*2}px`;
        imagen.style.height = 'auto';
        imagen.position = 'absolute';
        bubbleElement.appendChild(imagen);
        filling.appendChild(bubbleElement);
      });
      paginas[i].appendChild(filling); //Agregar el div de relleno a la página actual
    }
  });

</script>

<main>
  <div class="container">
    <div class="page intro">
      <h1>Pop the Top</h1>
      <h2>Los 5 álbumes nuevos más escuchados por año en las últimas dos décadas</h2>
      <img src="images/cheatguidedef.png" alt="cheatguide">
    </div>
    {#each anios as anio,index}
      <div class="page vis">
        <div class="info">
          {#each albums_of(anio) as album, index}
            <div class="album_container" style="width: {bubble_size(parseInt(album.Streams))}px; height: {bubble_size(parseInt(album.Streams))}px; top: {(posiciones_for(anio))[index][1]}px; left: {(posiciones_for(anio))[index][0]}px; animation-delay: {Math.random() * 3}s; animation-duration: {4 + Math.random() * 2}s;">      
              <div class="bubble">
                {#each posicion_circulos((genres(album.Generos).length)) as [x, y], index}
                  {#if genres(album.Generos).length != 1}
                    <div class="circle" style="left: {x}%; top: {y}% ; width: 75%; height: 75%; background-color: rgba({color_genero[genres(album.Generos)[index]][0]},{color_genero[genres(album.Generos)[index]][1]},{color_genero[genres(album.Generos)[index]][2]},{color_genero[genres(album.Generos)[index]][3]});"></div>
                  {/if}
                  {#if genres(album.Generos).length == 1}  
                    <div class="circle" style="transform: translate(0%, -5%); width: 110%; height: 110%; background-color: rgba({color_genero[genres(album.Generos)[index]][0]},{color_genero[genres(album.Generos)[index]][1]},{color_genero[genres(album.Generos)[index]][2]},{color_genero[genres(album.Generos)[index]][3]});"></div>
                  {/if}
                {/each}
                <a style="z-index:2" href="{album.Link}" target="_blank">
                  <img src="images/burbuja.png" alt="Bubble" style="width: {bubble_size(parseInt(album.Streams))}px; height: {bubble_size(parseInt(album.Streams))}px">
                </a>
                {#if album.Valoracion != 3}  
                  <img src="{recuadro_valoracion(album.Valoracion)}" alt="Circle" style="position: absolute; transform: translate(0%, -5.5%); max-width:112.5%; width: {bubble_size(parseInt(album.Streams))*1.125}px; height: {bubble_size(parseInt(album.Streams))*1.125}px">
                {/if}
                {#if album.aoty == 1}  
                  <div class="duck">
                    <img src="/images/patito.png" alt="Duck" style="max-width: {bubble_size(parseInt(album.Streams))*0.25}px; max-height: {bubble_size(parseInt(album.Streams))*0.25}px">
                  </div>
                {/if}
              </div>
              <div class="info_popup" style="top:-50%">
                <a href="{album.Link}" target="_blank" style="margin:5px; margin-bottom:1px">
                  <img src="{album.LinkImg}" alt="portada" class="album-img">
                </a>
                <p class="album-info" style="color:black; position:static; font-weight: 600; font-size: 14px">Streams: <span style="color:black; font-size: 14px">{streams_str(album.Streams)}</span><br>Géneros: <span style="color:black; font-size: 14px">{generos_str(album.Generos)}</span></p>
              </div>
              <p style="margin-top:20px;">{album["Album"]} <br><span>{album["Artista"]}</span></p>
            </div>
          {/each}
        </div>
        <div class = "anio">
          {#each anios_str[index] as caracter}
            <div class="caracter" style="animation: {4+Math.random()*2}s float ease-in-out infinite; animation-delay:{Math.random() * 3}s">
              <h1>{caracter}</h1>
            </div>
          {/each}
        </div>
        <div class="help">
          <img src="/images/boton_help_blue.png" alt="help" class="help_img" style="width: 35px; height:35px">          
          <div class="help_cuadro" style="width: 100vh; height:100%">
            <img src="/images/lil cheatguide.png" alt="mini cheat_sheet" style="border-radius: 20px;border: 2px solid white;">
          </div>
        </div>
      </div>
    {/each}
    <div class="page outro">
      <div>
        <h1>Desarrollado por</h1>
        <div class="redes_container">
          <div class="redes">
            <h1>Felicitas Astrada</h1>
            <a target="_blank" href="https://github.com/felicitasastrada">
              <img src="./images/git.png" alt="git bubble" style="animation: {4+Math.random()*2}s float ease-in-out infinite; animation-delay:{Math.random() * 3}s">
            </a>
            <a target="_blank" href="https://www.linkedin.com/in/felicitas-astrada-7040a3207/">
              <img src="./images/linkedin.png" alt="linkedin bubble" style="animation: {4+Math.random()*2}s float ease-in-out infinite; animation-delay:{Math.random() * 3}s">
            </a>
          </div>
          <div class="redes">
            <h1>Dafydd Jenkins</h1>
            <a target="_blank" href="https://github.com/Dafydd8">
              <img src="./images/git.png" alt="git bubble" style="animation: {4+Math.random()*2}s float ease-in-out infinite; animation-delay:{Math.random() * 3}s">
            </a>
            <a target="_blank" href="https://www.linkedin.com/in/dafydd-jenkins-7b696b331/">
              <img src="./images/linkedin.png" alt="linked in bubble" style="animation: {4+Math.random()*2}s float ease-in-out infinite; animation-delay:{Math.random() * 3}s">
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>

<style>
  .container {
    scroll-snap-type: y mandatory;
    overflow: hidden;
    overflow-y: scroll;
    width: 100%;
    height: 100vh;
  }
  
  .page {
    scroll-snap-align: start;
    padding: 2rem;
    width: 100%;
    height: 100%;
    display: flex;
    opacity: 0;
    transition: all 1s ease-in-out;
  }

  .intro {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .outro {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .info {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    max-width: 100%;
    max-height: 100%;
  }

  .album_container {
    position: absolute;
    width: auto;
    height: auto;
    animation: float ease-in-out infinite;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }
  
  .album_container:hover .info_popup {
    visibility: visible;
  }

  .album_container p {
    font-family: "Karla", sans-serif;
    font-optical-sizing: auto;
    font-weight: 400;
    font-style: normal;
    color: white;
    font-size: 18px;
    position: absolute;
    top: 95%;
    z-index: 1;
    text-wrap: nowrap;
  }

  .album_container span {
    font-family: "Karla", sans-serif;
    font-optical-sizing: auto;
    font-weight: 400;
    font-style: normal;
    font-size: 16px;
    color: #ebeaea;
  }

  .bubble {
    position: relative;
    width: auto;
    height: auto;
    display: flex;
    justify-content: center;
  }

  .bubble img {
    position: relative;
    z-index: 1;
  }

  .info_popup {
    position: absolute;
    visibility: hidden;
    z-index: 3;
    width: max-content;
    height:auto;
    background-color: white;
    opacity: 1;
    border-radius: 10px;
    display: flex;
    align-items: center; /* Alinea verticalmente la imagen y el texto */
    justify-content: center;

  }

  .info_popup img {
    width: 50px;
    height: 50px;
    border-radius: 10px;
  }

  .info_popup p {
    white-space: nowrap; /* Evita que el texto se divida en varias líneas */
    margin: 5px;
    text-align: left;
  }

  .duck {
    animation: bounce2 2s infinite;
    position: absolute;
    z-index: 2;
    top: -20%;
  }

  .circle {
    position: absolute;
    border-radius: 50%;
    filter: blur(10px);
    transform: translate(15%, 15%);
    z-index: 0;
  }

  .anio {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    top: 85%;
    left: 85%;
    max-width: 100px;
    max-height: 100px;
  }

  h1 {
    font-family: 'Bubbly', sans-serif;
    font-size: 3rem;
    color: white;
  }
  h2 {
    font-family: 'Bubbly', sans-serif;
    font-size: 1.75rem;
    color: white;
  }

  .help {
    position:relative; 
    left: 87.5%;
    height:fit-content;
  } 

  .help_cuadro {
    position:absolute;
    transform: translateX(-100%);
    visibility: hidden;
    max-height: 100%;
    z-index: 3;
  }

  .help:hover .help_cuadro {
    visibility: visible;
  }

  .redes_container {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
    width:100%;
    gap: 100px;
  }

  .redes a {
    margin: 10px;
  }

  .redes a img{
    margin-top: 5%;
  }

</style>
