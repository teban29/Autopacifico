let container = document.querySelector(".container");
let btn = document.getElementById("spin");
const overlay = document.getElementById("overlay");

// Configurar premios con probabilidades iniciales
let premios = [
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $50,000", probabilidad: 8 },
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $100,000", probabilidad: 10 },
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $150,000", probabilidad: 4 },
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $200,000", probabilidad: 2 },
];

// Normalizar probabilidades
let total = premios.reduce((sum, premio) => sum + premio.probabilidad, 0);
premios = premios.map(premio => ({
    ...premio,
    probabilidadNormalizada: premio.probabilidad / total,
}));

// Función para seleccionar un premio basado en probabilidades normalizadas
function seleccionarPremio() {
    let random = Math.random(); // Número aleatorio entre 0 y 1
    let acumulado = 0;

    for (let i = 0; i < premios.length; i++) {
        acumulado += premios[i].probabilidadNormalizada;
        if (random <= acumulado) {
            return i; // Retorna el índice del premio seleccionado
        }
    }
    return premios.length - 1; // Fallback al último premio
}

// Si ya hay un resultado, deshabilitar interacción y mostrar overlay
if (btn.disabled) {
    overlay.classList.add("mostrar");
}

btn.onclick = function () {
    let seleccionado = seleccionarPremio(); // Determina el índice del premio
    let gradosPorSegmento = 360 / premios.length; // Grados de cada segmento
    let gradosSeleccionados = gradosPorSegmento * seleccionado; // Grados donde comienza el segmento seleccionado
    let ajusteInicial = 22.5; // Compensación para alinear el primer segmento con la flecha
    let rotacionFinal = (360 * 5) + (360 - (gradosSeleccionados + ajusteInicial)); // Giros completos + ajuste

    // Rotar la ruleta
    container.style.transform = `rotate(${rotacionFinal}deg)`;

    // Bloquear el botón inmediatamente
    btn.disabled = true;

    // Mostrar el mensaje después de la animación de la ruleta
    setTimeout(() => {
        const premioGanado = premios[seleccionado].nombre;

        // Mostrar mensaje dependiendo del premio
        if (premioGanado === "Gracias por participar") {
            mostrarMensajeSinPremio("😞 Gracias por participar, ¡mejor suerte la próxima vez!");
        } else {
            mostrarMensajePremio(`🎉 ¡Felicidades! Ganaste ${premioGanado} 🎉`);
        }

        // Retrasar el efecto de difuminado hasta después de la animación
        setTimeout(() => {
            overlay.classList.add("mostrar");
        }, 10);

        // Guardar resultado en el servidor
        fetch(resultadoUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ premio: premioGanado }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error al guardar el resultado");
                }
                return response.json();
            })
            .then(data => console.log("Resultado guardado:", data))
            .catch(error => {
                console.error("Error al enviar el resultado:", error);
                alert("No se pudo guardar el resultado. Intenta de nuevo.");
            });
    }, 5000); // Tiempo de espera por la animación de la ruleta
};

// Función para mostrar mensaje de premio
function mostrarMensajePremio(mensaje) {
    const mensajePremio = document.getElementById("mensaje-premio");
    mensajePremio.textContent = mensaje;
    mensajePremio.classList.remove("oculto");
    mensajePremio.classList.add("mostrar");
}

// Función para mostrar mensaje de sin premio
function mostrarMensajeSinPremio(mensaje) {
    const mensajeSinPremio = document.getElementById("mensaje-sin-premio");
    mensajeSinPremio.textContent = mensaje;
    mensajeSinPremio.classList.remove("oculto");
    mensajeSinPremio.classList.add("mostrar");
}
