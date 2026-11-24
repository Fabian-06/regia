"""Tests del asistente. Responsable: persona 4.

PENDIENTE. Los tests no deben llamar al LLM real (cuesta dinero y no es
determinista): sustituid assistant.llm.complete con unittest.mock.

Comprobaciones útiles:

- Con una respuesta simulada del LLM, parse_query() devuelve el RouteRequest
  esperado.
- Si el LLM devuelve una estación que no existe, ValueError.
- Sin clave configurada, parse_query() funciona en modo sin LLM.
- explain() en modo sin LLM incluye el tiempo total y los transbordos.

Se ejecutan con: python manage.py test assistant
"""
from core.contracts import Algorithm,Context,Graph,Incident,IncidentKind,Profile,RouteResult,RouteStep,StationInfo
from unittest import TestCase
from assistant.parser import parse_query
from assistant.explainer import explain
from datetime import datetime, timezone
from unittest.mock import patch


def make_test_graph() -> Graph:
    nombres = {"talleres": "Talleres",
                "exposicion": "Exposición",
                "sendero": "Sendero",
                "hospital": "Hospital",
                "hospital-metropolitano": "Hospital Metropolitano",
                "general-anaya": "General Anaya",
                "general-i-zaragoza": "General I. Zaragoza",
                "felix-u-gomez": "Félix U. Gómez"}
    stations = {
        station_id: StationInfo(
            id=station_id,
            name=name,
            lat=0.0,
            lon=0.0,
            line_ids=("L1",),
            underground=False,
            has_elevator=True,
        ) for station_id, name in nombres.items()
    }
    return Graph(stations=stations, lines={}, edges={})

@patch("assistant.llm.is_available", new=lambda: False)
class TestParserSinLLM(TestCase):
    def setUp(self):
        self.graph = make_test_graph()
    def test_basico_con_tilde(self):
        req = parse_query("de Talleres a Exposición", self.graph)
        self.assertEqual(req.origin, "talleres")
        self.assertEqual(req.destination, "exposicion")
        self.assertEqual(req.profile, Profile.FASTEST)
    def test_accesible_hospital(self):
        req = parse_query("Voy en silla de ruedas del Hospital a Sendero",self.graph)
        self.assertEqual(req.origin, "hospital")
        self.assertEqual(req.destination, "sendero")
        self.assertEqual(req.profile, Profile.ACCESSIBLE)
    def test_hospital_metropolitano(self):
        req = parse_query("de Talleres al Hospital Metropolitano", self.graph)
        self.assertEqual(req.origin, "talleres")
        self.assertEqual(req.destination, "hospital-metropolitano")
        self.assertEqual(req.profile, Profile.FASTEST)
    def test_menos_transbordos_abreviatura(self):
        req = parse_query("de Sendero a Félix U. Gómez sin transbordos", self.graph)
        self.assertEqual(req.origin, "sendero")
        self.assertEqual(req.destination, "felix-u-gomez")
        self.assertEqual(req.profile, Profile.FEWEST_TRANSFERS)
    def test_orden_invertido(self):
        req = parse_query("Quiero ir a Exposición desde Talleres", self.graph)
        self.assertEqual(req.origin, "talleres")
        self.assertEqual(req.destination, "exposicion")
        self.assertEqual(req.profile, Profile.FASTEST)
    def test_sin_destino(self):
        with self.assertRaises(ValueError):
            parse_query("Salgo de talleres", self.graph)
    def test_ruta_con_transbordo_e_incidencia(self):
        steps = (RouteStep(station_id="talleres", line_id="L1", minutes=0.0),
            RouteStep(station_id="hospital", line_id="L1", minutes=6.0),
            RouteStep(station_id="hospital", line_id="L2", minutes=9.5),
            RouteStep(station_id="sendero", line_id="L2", minutes=14.5))
        result = RouteResult(
            found=True,
            steps=steps,
            total_minutes=14.5,
            transfers=1,
            nodes_expanded=5,
            algorithm=Algorithm.ASTAR,
        )
        incidencia = Incident(
            kind=IncidentKind.LINE_DELAY,
            station_id=None,
            line_id="L2",
            extra_minutes=8.0,
            description="Retraso en Línea 2",
        )
        context = Context(
            when=datetime.now(timezone.utc),
            service_open=True,
            headways={"L1": 5.0, "L2": 6.0},
            weather=None,
            incidents=(incidencia,),
        )
        texto = explain(result, context, self.graph)
        self.assertIn("Talleres", texto)
        self.assertIn("Sendero", texto)
        self.assertIn("14.5", texto)
        self.assertIn("1", texto)
        self.assertIn("Hospital", texto)
        self.assertIn("Retraso en Línea 2", texto)
    def test_ruta_sin_transbordos(self):
        steps = (RouteStep(station_id="talleres", line_id="L1", minutes=0.0),
                RouteStep(station_id="exposicion", line_id="L1", minutes=8.0))
        result = RouteResult(
            found=True,
            steps=steps,
            total_minutes=8.0,
            transfers=0,
            nodes_expanded=2,
            algorithm=Algorithm.ASTAR,
        )
        context = Context(
            when=datetime.now(timezone.utc),
            service_open=True,
            headways={"L1": 8.0},
            weather=None,
            incidents=()
        )
        texto = explain(result, context, self.graph)
        self.assertIn("Talleres", texto)
        self.assertIn("Exposición", texto)
        self.assertIn("8.0", texto)
        self.assertIn("sin transbordos", texto)
        self.assertNotIn("Incidencias",texto)
    def test_sin_ruta(self):
        result = RouteResult(
            found=False,
            steps=(),
            total_minutes=0.0,
            transfers=0,
            nodes_expanded=0,
            algorithm=Algorithm.ASTAR,
        )
        context = Context(
            when=datetime.now(timezone.utc),
            service_open=False,
            headways={},
            weather=None,
            incidents=()
        )
        texto = explain(result, context, self.graph)
        self.assertIn("cerrado",texto)
        incidencia = Incident(
            kind=IncidentKind.STATION_CLOSED,
            station_id="hospital",
            line_id=None,
            extra_minutes=0.0,
            description="Estación Hospital cerrada",
        )
        context2 = Context(
            when=datetime.now(timezone.utc),
            service_open=True,
            headways={},
            weather=None,
            incidents=(incidencia,),
        )
        texto2 = explain(result, context2, self.graph)
        self.assertIn("No hay una ruta", texto2)
        self.assertIn("Estación Hospital cerrada",texto2)

@patch("assistant.llm.is_available", new=lambda: True)
@patch("assistant.llm.complete")
class TestAsistenteConLLM(TestCase):
    def setUp(self):
        self.graph = make_test_graph()
    def test_con_llm_ok(self,mock_complete):
        mock_complete.return_value = ('{"origin": "talleres", "destination": "hospital-metropolitano", '
            '"profile": "accessible"}')
        req = parse_query("quiero ir al hospital grande en silla", self.graph)
        self.assertEqual(req.origin, "talleres")
        self.assertEqual(req.destination, "hospital-metropolitano")
        self.assertEqual(req.profile, Profile.ACCESSIBLE)
    def test_con_llm_estacion_inventada(self, mock_complete):
        mock_complete.return_value = ('{"origin": "talleres", "destination": "narnia", "profile": "fastest"}')
        with self.assertRaises(ValueError):
            parse_query("de Talleres a Sol", self.graph)
    def test_si_llm_falla(self, mock_complete):
        mock_complete.side_effect = RuntimeError("timeout")
        req = parse_query("de Talleres a Exposición", self.graph)
        self.assertEqual(req.origin, "talleres")
        self.assertEqual(req.destination, "exposicion")
    def test_explicar_llm(self, mock_complete):
        steps = (
            RouteStep(station_id="talleres", line_id="L1", minutes=0.0),
            RouteStep(station_id="exposicion", line_id="L1", minutes=8.0),
        )
        result = RouteResult(
            found=True, steps=steps, total_minutes=8.0, transfers=0,
            nodes_expanded=2, algorithm=Algorithm.ASTAR,
        )
        context = Context(
            when=datetime.now(timezone.utc), service_open=True,
            headways={"L1": 8.0}, weather=None, incidents=(),
        )

        mock_complete.return_value = "Ruta directa y rápida."
        self.assertEqual(explain(result, context, self.graph), "Ruta directa y rápida.")

        mock_complete.side_effect = RuntimeError("caído")
        texto = explain(result, context, self.graph)
        self.assertIn("8.0", texto)
        self.assertIn("sin transbordos", texto)