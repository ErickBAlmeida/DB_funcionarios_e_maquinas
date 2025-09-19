import os
from tkinter import messagebox

import customtkinter as ctk

import banco
from dicts import *


class DatabaseApp:
    def __init__(self, banco):
        self.banco = banco

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.janela = ctk.CTk()
        self.janela.title("Sistema de Gerenciamento - Funcionários e Máquinas")
        self.janela.geometry("1200x700")

        self.tema_atual = "dark"
        self.setup_ui()

    def setup_ui(self):
        self.criar_side_bar()
        self.criar_main_frame()
        self.criar_botoes()
        self.criar_content_area()
        self.mostrar_home()

    def criar_side_bar(self):
        self.frame_lateral = ctk.CTkFrame(self.janela, width=250)
        self.frame_lateral.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(self.frame_lateral, text="Painel de Controle",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

    def criar_main_frame(self):
        self.frame_principal = ctk.CTkScrollableFrame(self.janela)
        self.frame_principal.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(self.frame_principal, text="🏢 Sistema de Gerenciamento",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(20,10))

    def criar_botoes(self):
        self._criar_botao_lateral("🏠 Home", self.mostrar_home, "#2d5a27", "#1f3d1b")
        self.btn_tema = self._criar_botao_lateral(
            "🌙 Tema Escuro", self.alternar_tema, "#444", "#333"
        )

        # Seções
        self._criar_secao_lateral("👥 FUNCIONÁRIOS", [
            ("➕ Inserir Funcionário", "inserir_funcionario"),
            ("🧹 apagar Funcionário", "apagar_funcionario"),
            ("📋 Listar Funcionários", "listar_funcionarios")
        ])
        self._criar_secao_lateral("🔧 MÁQUINAS", [
            ("➕ Inserir Máquina", "inserir_maquina"),
            ("🧹 apagar Máquina", "apagar_maquina"),
            ("📋 Listar Máquinas", "listar_maquinas")
        ])

    def _criar_botao_lateral(self, texto, comando, fg="#444", hover="#333"):
        btn = ctk.CTkButton(self.frame_lateral, text=texto, command=comando,
                             width=220, height=40,
                             font=ctk.CTkFont(size=14, weight="bold"),
                             fg_color=fg, hover_color=hover)
        btn.pack(pady=8)
        return btn

    def _criar_secao_lateral(self, titulo, botoes):
        ctk.CTkLabel(self.frame_lateral, text=titulo, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,5))
        for txt, cmd in botoes:
            ctk.CTkButton(self.frame_lateral, text=txt, command=lambda x=cmd: self.mostrar_pagina(x),
                           width=220, height=35, font=ctk.CTkFont(size=12)).pack(pady=3)
        ctk.CTkFrame(self.frame_lateral, height=1, fg_color="gray70").pack(fill="x", padx=20, pady=10)

    def criar_content_area(self):
        self.frame_conteudo = ctk.CTkFrame(self.frame_principal)
        self.frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)
        self.area_principal = ctk.CTkFrame(self.frame_conteudo)
        self.area_principal.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------------- Utils ----------------
    def limpar_area_principal(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    def criar_campo(self, container, label_text, tipo="entry", valores=None):
        frame = ctk.CTkFrame(container, fg_color="transparent")
        frame.pack(pady=5, fill="x", padx=20)
        ctk.CTkLabel(frame, text=label_text, width=120, anchor="e").pack(side="left", padx=5)
        if tipo=="entry":
            widget = ctk.CTkEntry(frame, width=250, height=35)
        else:  # dropdown
            widget = ctk.CTkOptionMenu(frame, values=valores or [], width=250, height=35)
            widget.set(valores[0] if valores else "")
        widget.pack(side="left", padx=5)
        return widget

    def criar_item_lista(self, container, titulo, info_dict, excluir_cmd):
        item_frame = ctk.CTkFrame(container)
        item_frame.pack(fill="x", padx=10, pady=5)
        info_frame = ctk.CTkFrame(item_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(info_frame, text=titulo, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        for k,v in info_dict.items():
            ctk.CTkLabel(info_frame, text=f"{k}: {v}").pack(anchor="w")
        ctk.CTkButton(item_frame, text="🗑️ Excluir", command=excluir_cmd,
                       width=80, height=30, fg_color="red", hover_color="darkred").pack(side="right", padx=10, pady=10)

    # ---------------- Temas ----------------
    def alternar_tema(self):
        self.tema_atual = "light" if self.tema_atual=="dark" else "dark"
        ctk.set_appearance_mode(self.tema_atual)
        self.btn_tema.configure(text="🌙 Tema Escuro" if self.tema_atual=="dark" else "☀️ Tema Claro")

    # ---------------- Páginas ----------------
    def mostrar_home(self):
        self.limpar_area_principal()
        ctk.CTkLabel(self.area_principal, text="⭐ Sistema de Gerenciamento",
                     font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)
        ctk.CTkLabel(self.area_principal, text="✨ Gerencie funcionários e máquinas de forma eficiente",
                     font=ctk.CTkFont(size=16)).pack(pady=10)

    def mostrar_pagina(self, nome):
        paginas = {
            "inserir_funcionario": self.mostrar_inserir_funcionario,
            "apagar_funcionario": self.mostrar_apagar_funcionario,
            "listar_funcionarios": self.mostrar_listar_funcionarios,
            "inserir_maquina": self.mostrar_inserir_maquina,
            "apagar_maquina": self.mostrar_apagar_maquina,
            "listar_maquinas": self.mostrar_listar_maquinas
        }
        if nome in paginas: paginas[nome]()    

    # ---------------- Funcionários ----------------
    def mostrar_inserir_funcionario(self):
        self.limpar_area_principal()
        ctk.CTkLabel(self.area_principal, text="➕ Inserir Novo Funcionário",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        form = ctk.CTkFrame(self.area_principal)
        form.pack(pady=20, padx=100, fill="x")
        self.emp_nome = self.criar_campo(form, "Nome:")
        self.emp_cpf = self.criar_campo(form, "CPF:")
        self.emp_departamento = self.criar_campo(form, "Departamento:", "dropdown", lista_departamentos)
        self.emp_cargo = self.criar_campo(form, "Cargo:", "dropdown", lista_cargos)
        self.emp_contrato = self.criar_campo(form, "Contrato:", "dropdown", lista_contratos)
        self.emp_email = self.criar_campo(form, "E-mail:")
        self.emp_maquina = self.criar_campo(form, "Maquina:")
        ctk.CTkButton(form, text="✅ Inserir Funcionário", command=lambda: self.banco.inserir_dados(
            "Colaboradores",
            dados= {
                "nome" : self.emp_nome.get(),
                "CPF" : self.emp_cpf.get(),
                "email" : self.emp_email.get(),
                "Departamento" : self.emp_departamento.get(),
                "Cargo" : self.emp_cargo.get(),
                "Contrato" : self.emp_contrato.get(),
                "Maquina" : self.emp_maquina.get(),
            }
        ),
                       width=200, height=40, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)

    def mostrar_apagar_funcionario(self):
        self.limpar_area_principal()
        ctk.CTkLabel(self.area_principal, text="🧹 apagar Funcionário",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        form = ctk.CTkFrame(self.area_principal)
        form.pack(pady=20, padx=100, fill="x")
        
        # Campo de busca por nome
        self.buscar_nome = self.criar_campo(form, "Nome completo do Funcionário:")
        
        # Botão para carregar dados
        ctk.CTkButton(form, text="🔍 Buscar", command=lambda: self.banco.remover_dados("Colaboradores", self.buscar_nome.get()),
                    width=150, height=35).pack(pady=10)

    def mostrar_listar_funcionarios(self): pass

    # ---------------- Máquinas ----------------
    def mostrar_inserir_maquina(self):
        self.limpar_area_principal()
        ctk.CTkLabel(self.area_principal, text="➕ Inserir Nova Máquina",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        form = ctk.CTkFrame(self.area_principal)
        form.pack(pady=20, padx=100, fill="x")
        self.maq_placa = self.criar_campo(form, "Placa:")
        self.maq_marca = self.criar_campo(form, "Marca:", "dropdown", lista_marcas_maquinas)
        self.maq_modelo = self.criar_campo(form, "Modelo:", "dropdown", lista_modelos_maquinas)
        self.maq_RAM = self.criar_campo(form, "RAM:")
        self.maq_anydesk = self.criar_campo(form, "AnyDesk:")
        ctk.CTkButton(form, text="✅ Inserir Máquina", command=lambda: self.banco.inserir_dados(
            "Maquinas",
            dados = {
                "Placa": self.maq_placa.get(),
                "Marca": self.maq_marca.get(),
                "Modelo": self.maq_modelo.get(),
                "RAM": self.maq_RAM.get(),
                "anydesk": self.maq_anydesk.get(),
            }
        ),
                       width=200, height=40, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)
        
    def mostrar_apagar_maquina(self):
        self.limpar_area_principal()
        ctk.CTkLabel(self.area_principal, text="🧹 Apagar máquina",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        form = ctk.CTkFrame(self.area_principal)
        form.pack(pady=20, padx=100, fill="x")
        
        # Campo de busca por placa
        self.buscar_placa = self.criar_campo(form, "Placa da Máquina:")
        
        # Botão para carregar dados
        ctk.CTkButton(form, text="🔍 Buscar", command=lambda: self.banco.remover_dados("Maquinas", self.buscar_placa.get()),
                    width=150, height=35).pack(pady=10)
        
    def mostrar_listar_maquinas(self): pass

    # ---------------- Iniciar ----------------
    def iniciar(self): self.janela.mainloop()


if __name__=="__main__":
    banco = banco.Banco()
    app = DatabaseApp(banco)
    app.iniciar()
