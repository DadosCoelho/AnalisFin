"""
AnalisFin - Sistema de Análise de Mercado Financeiro
Autor: Sistema de Análise Automatizada
Data: 2025

Ponto de entrada principal da aplicação.
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from config.settings import Config
from core.period_manager import PeriodManager
from core.query_scheduler import QueryScheduler
from core.data_fetcher import DataFetcher
from core.csv_writer import CSVWriter
from core.analyzer import Analyzer
from utils.helpers import list_csv_files, generate_chart
import os

console = Console()

class AnalisFin:
    """Classe principal do sistema AnalisFin"""
    
    def __init__(self):
        """Inicializa o sistema"""
        self.config = Config()
        self.running = True
    
    def show_banner(self):
        """Exibe banner inicial"""
        banner = """
╔═══════════════════════════════════════╗
║      AnalisFin v1.0                   ║
║   Análise de Mercado Financeiro       ║
╚═══════════════════════════════════════╝
        """
        console.print(Panel(banner, style="bold blue"))
    
    def show_menu(self):
        """Exibe menu principal"""
        console.print("\n[bold cyan]MENU PRINCIPAL[/bold cyan]")
        console.print("1 - Configurar parâmetros")
        console.print("2 - Executar análise")
        console.print("3 - Ver CSVs salvos")
        console.print("4 - Gerar gráficos")
        console.print("5 - Sair")
        console.print()
    
    def configure_parameters(self):
        """Configura parâmetros do sistema"""
        console.print("\n[bold yellow]CONFIGURAÇÃO DE PARÂMETROS[/bold yellow]\n")
        
        # Símbolo
        symbol = Prompt.ask("Símbolo (ex: BTCUSDT, AAPL)", default=self.config.symbol)
        
        # Período
        console.print("\nExemplos: 5min, 10min, 1hora, 1dia, 1semana")
        period = Prompt.ask("Período", default=self.config.period)
        
        # Quantidade de consultas
        qtd_consultas = IntPrompt.ask(
            "Quantidade de consultas por período",
            default=self.config.qtd_consultas
        )
        
        # Quantidade de períodos
        qtd_periodo = IntPrompt.ask(
            "Quantidade de períodos a analisar",
            default=self.config.qtd_periodo
        )
        
        # API provider
        console.print("\nAPIs disponíveis: binance, polygon, yahoo, alphavantage")
        api_provider = Prompt.ask("API provider", default=self.config.api_provider)
        
        # Atualiza configurações
        self.config.update(
            symbol=symbol,
            period=period,
            qtd_consultas=qtd_consultas,
            qtd_periodo=qtd_periodo,
            api_provider=api_provider
        )
        
        console.print("\n[bold green]✓ Parâmetros configurados com sucesso![/bold green]")
        self.config.display()
    
    def execute_analysis(self):
        """Executa análise completa"""
        console.print("\n[bold yellow]EXECUTANDO ANÁLISE...[/bold yellow]\n")
        
        try:
            # 1. Gerenciar períodos
            console.print("[cyan]► Calculando janelas de tempo...[/cyan]")
            period_manager = PeriodManager(self.config)
            periods = period_manager.generate_periods()
            console.print(f"  ✓ {len(periods)} períodos gerados")
            
            # 2. Agendar consultas
            console.print("[cyan]► Agendando consultas...[/cyan]")
            scheduler = QueryScheduler(self.config)
            queries = scheduler.schedule_queries(periods)
            console.print(f"  ✓ {len(queries)} consultas agendadas")
            
            # 3. Buscar dados
            console.print("[cyan]► Coletando dados do mercado...[/cyan]")
            fetcher = DataFetcher(self.config)
            market_data = fetcher.fetch_all(queries)
            console.print(f"  ✓ {len(market_data)} registros coletados")
            
            # 4. Salvar em CSV
            console.print("[cyan]► Salvando dados em CSV...[/cyan]")
            writer = CSVWriter(self.config)
            csv_path = writer.save(market_data)
            console.print(f"  ✓ Arquivo salvo: {csv_path}")
            
            # 5. Analisar dados
            console.print("[cyan]► Analisando tendências...[/cyan]")
            analyzer = Analyzer(self.config)
            result = analyzer.analyze(csv_path)
            
            # 6. Exibir resultado
            self.display_results(result)
            
        except Exception as e:
            console.print(f"\n[bold red]✗ Erro: {str(e)}[/bold red]")
    
    def display_results(self, result):
        """Exibe resultados da análise"""
        console.print("\n" + "="*50)
        console.print("[bold green]RESULTADO DA ANÁLISE[/bold green]")
        console.print("="*50 + "\n")
        
        console.print(f"[cyan]Tendência:[/cyan] {result['tendencia']}")
        console.print(f"[cyan]Curva:[/cyan] {result['curva']:.2f}/100")
        console.print(f"[cyan]Probabilidade de Alta:[/cyan] {result['prob_alta']:.2f}%")
        console.print(f"[cyan]Probabilidade de Baixa:[/cyan] {result['prob_baixa']:.2f}%")
        console.print(f"[cyan]Arquivo CSV:[/cyan] {result['arquivo_csv']}")
        console.print()
    
    def list_csvs(self):
        """Lista CSVs salvos"""
        console.print("\n[bold yellow]CSVs SALVOS[/bold yellow]\n")
        files = list_csv_files()
        
        if not files:
            console.print("[yellow]Nenhum arquivo CSV encontrado.[/yellow]")
        else:
            for i, file in enumerate(files, 1):
                console.print(f"{i}. {file}")
    
    def generate_charts(self):
        """Gera gráficos dos dados"""
        console.print("\n[bold yellow]GERAÇÃO DE GRÁFICOS[/bold yellow]\n")
        
        files = list_csv_files()
        if not files:
            console.print("[yellow]Nenhum CSV disponível para gráficos.[/yellow]")
            return
        
        console.print("Arquivos disponíveis:")
        for i, file in enumerate(files, 1):
            console.print(f"{i}. {file}")
        
        choice = IntPrompt.ask("\nEscolha um arquivo (número)", choices=[str(i) for i in range(1, len(files)+1)])
        
        csv_path = os.path.join("data", "csvs", files[choice-1])
        generate_chart(csv_path)
        console.print("\n[green]✓ Gráfico gerado com sucesso![/green]")
    
    def run(self):
        """Loop principal da aplicação"""
        self.show_banner()
        
        while self.running:
            self.show_menu()
            choice = Prompt.ask("Escolha uma opção", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                self.configure_parameters()
            elif choice == "2":
                self.execute_analysis()
            elif choice == "3":
                self.list_csvs()
            elif choice == "4":
                self.generate_charts()
            elif choice == "5":
                console.print("\n[bold blue]Encerrando AnalisFin... Até logo![/bold blue]")
                self.running = False
            
            if self.running:
                input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    app = AnalisFin()
    app.run()
