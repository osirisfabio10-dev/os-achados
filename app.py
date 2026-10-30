
import streamlit as st
import pandas as pd
from pathlib import Path

# =====================================
# CONFIGURAÇÕES
# =====================================

NOME_LOJA = "OS ACHADOS"

# TROQUE PELA SUA SENHA
SENHA_ADMIN = "372114"

ARQUIVO = Path(__file__).parent / "produtos.csv"

COLUNAS = [
    "nome",
    "preco",
    "imagem_url",
    "link_ml",
    "categoria",
    "destaque"
]

st.set_page_config(
    page_title="OS ACHADOS",
    page_icon="🛍️",
    layout="wide"
)

# =====================================
# VISUAL DA LOJA
# =====================================

st.markdown("""
<style>
.stApp {
    background-color: #101010;
    color: white;
}

[data-testid="stHeader"] {
    background-color: #101010;
}

.logo {
    text-align: center;
    color: #FFE600;
    font-size: 48px;
    font-weight: 900;
    letter-spacing: 3px;
    padding-top: 25px;
}

.subtitulo {
    text-align: center;
    color: #cccccc;
    font-size: 17px;
    margin-bottom: 25px;
}

.secao {
    color: #FFE600;
    font-size: 25px;
    font-weight: bold;
    margin-top: 25px;
}

.preco {
    color: #FFE600;
    font-size: 25px;
    font-weight: 900;
}

div.stLinkButton > a {
    background-color: #FFE600;
    color: #111111;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    width: 100%;
}

.rodape {
    text-align: center;
    color: #999999;
    padding: 35px 10px;
    margin-top: 40px;
    border-top: 1px solid #333333;
}
</style>
""", unsafe_allow_html=True)


# =====================================
# FUNÇÕES DOS PRODUTOS
# =====================================

def carregar_produtos():
    if not ARQUIVO.exists():
        pd.DataFrame(columns=COLUNAS).to_csv(
            ARQUIVO,
            index=False,
            encoding="utf-8-sig"
        )

    try:
        dados = pd.read_csv(ARQUIVO, encoding="utf-8-sig")
    except pd.errors.EmptyDataError:
        dados = pd.DataFrame(columns=COLUNAS)

    for coluna in COLUNAS:
        if coluna not in dados.columns:
            dados[coluna] = ""

    return dados[COLUNAS]


def salvar_produtos(dados):
    dados.to_csv(
        ARQUIVO,
        index=False,
        encoding="utf-8-sig"
    )


# =====================================
# PAINEL ADMINISTRATIVO
# =====================================

st.sidebar.title("🔐 Administração")

senha_digitada = st.sidebar.text_input(
    "Senha do administrador",
    type="password"
)

if senha_digitada == SENHA_ADMIN:
    st.sidebar.success("Acesso autorizado!")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Cadastrar produto")

    with st.sidebar.form("formulario_produto"):

        nome = st.text_input("Nome do produto")

        preco = st.number_input(
            "Preço (R$)",
            min_value=0.01,
            value=49.90,
            step=1.00
        )

        imagem_url = st.text_input(
            "Link da imagem"
        )

        link_ml = st.text_input(
            "Link de compra"
        )

        categoria = st.selectbox(
            "Categoria",
            [
                "Eletrônicos",
                "Casa",
                "Acessórios",
                "Beleza",
                "Moda",
                "Outros"
            ]
        )

        destaque = st.checkbox(
            "Colocar nos destaques"
        )

        cadastrar = st.form_submit_button(
            "CADASTRAR PRODUTO",
            use_container_width=True
        )

        if cadastrar:

            if not nome.strip():
                st.error("Digite o nome do produto.")

            elif not imagem_url.startswith(("http://", "https://")):
                st.error("Digite um link válido para a imagem.")

            elif not link_ml.startswith(("http://", "https://")):
                st.error("Digite um link válido para a compra.")

            else:
                dados = carregar_produtos()

                novo_produto = pd.DataFrame([{
                    "nome": nome.strip(),
                    "preco": preco,
                    "imagem_url": imagem_url.strip(),
                    "link_ml": link_ml.strip(),
                    "categoria": categoria,
                    "destaque": "sim" if destaque else "nao"
                }])

                dados = pd.concat(
                    [dados, novo_produto],
                    ignore_index=True
                )

                salvar_produtos(dados)

                st.sidebar.success(
                    "Produto cadastrado com sucesso!"
                )

                st.rerun()

    # =================================
    # EXCLUIR PRODUTO
    # =================================

    st.sidebar.markdown("---")
    st.sidebar.subheader("Excluir produto")

    dados = carregar_produtos()

    if not dados.empty:

        indice = st.sidebar.selectbox(
            "Escolha o produto",
            options=list(dados.index),
            format_func=lambda i: str(dados.loc[i, "nome"]),
            key="produto_para_excluir"
        )

        if st.sidebar.button(
            "EXCLUIR PRODUTO",
            use_container_width=True
        ):
            dados = dados.drop(index=indice).reset_index(drop=True)
            salvar_produtos(dados)

            st.sidebar.success("Produto excluído!")
            st.rerun()

    else:
        st.sidebar.info("Ainda não existem produtos.")

elif senha_digitada:
    st.sidebar.error("Senha incorreta.")


# =====================================
# CARREGAR PRODUTOS
# =====================================

produtos = carregar_produtos()

produtos["preco"] = pd.to_numeric(
    produtos["preco"],
    errors="coerce"
)

produtos["destaque"] = (
    produtos["destaque"]
    .astype(str)
    .str.strip()
    .str.lower()
)

produtos = produtos.dropna(subset=["nome", "preco"])


# =====================================
# CABEÇALHO
# =====================================

st.markdown(
    f'<div class="logo">{NOME_LOJA}</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="subtitulo">
    Os melhores achados, ofertas e produtos para você!
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background:#222;
    padding:15px;
    border-radius:10px;
    text-align:center;
    margin-bottom:25px;">
    🛍️ Produtos selecionados • Ofertas especiais • Compre online
</div>
""", unsafe_allow_html=True)


# =====================================
# PESQUISA E CATEGORIAS
# =====================================

st.markdown(
    '<div class="secao">ENCONTRE SEU ACHADO</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([2, 1])

with col1:
    pesquisa = st.text_input(
        "Pesquisar",
        placeholder="Digite o nome do produto..."
    )

with col2:
    categorias = sorted(
        produtos["categoria"].dropna().astype(str).unique()
    )

    categoria = st.selectbox(
        "Categoria",
        ["Todas"] + categorias
    )


filtrados = produtos.copy()

if pesquisa:
    filtrados = filtrados[
        filtrados["nome"].astype(str).str.contains(
            pesquisa,
            case=False,
            na=False
        )
    ]

if categoria != "Todas":
    filtrados = filtrados[
        filtrados["categoria"] == categoria
    ]


# =====================================
# DESTAQUES
# =====================================

destaques = filtrados[
    filtrados["destaque"] == "sim"
]

if not pesquisa and categoria == "Todas":

    st.markdown(
        '<div class="secao">⭐ DESTAQUES</div>',
        unsafe_allow_html=True
    )

    if not destaques.empty:

        colunas = st.columns(3)

        for indice, (_, produto) in enumerate(destaques.iterrows()):

            with colunas[indice % 3]:

                with st.container(border=True):

                    st.image(
                        str(produto["imagem_url"]),
                        width="stretch"
                    )

                    st.caption("⭐ PRODUTO EM DESTAQUE")

                    st.subheader(str(produto["nome"]))

                    st.markdown(
                        f'<div class="preco">R$ {produto["preco"]:.2f}</div>',
                        unsafe_allow_html=True
                    )

                    st.link_button(
                        "COMPRAR AGORA",
                        str(produto["link_ml"]),
                        width="stretch"
                    )


# =====================================
# TODOS OS PRODUTOS
# =====================================

st.markdown(
    '<div class="secao">🛒 TODOS OS PRODUTOS</div>',
    unsafe_allow_html=True
)

if filtrados.empty:

    st.warning("Nenhum produto encontrado.")

else:

    colunas = st.columns(3)

    for indice, (_, produto) in enumerate(filtrados.iterrows()):

        with colunas[indice % 3]:

            with st.container(border=True):

                st.image(
                    str(produto["imagem_url"]),
                    width="stretch"
                )

                st.subheader(str(produto["nome"]))

                st.caption(
                    f"Categoria: {produto['categoria']}"
                )

                st.markdown(
                    f'<div class="preco">R$ {produto["preco"]:.2f}</div>',
                    unsafe_allow_html=True
                )

                st.link_button(
                    "VER OFERTA NO MERCADO LIVRE",
                    str(produto["link_ml"]),
                    width="stretch"
                )


# =====================================
# RODAPÉ
# =====================================

st.markdown("""
<div class="rodape">
    <h3 style="color:#FFE600;">OS ACHADOS</h3>
    <p>Encontre produtos incríveis em um só lugar.</p>
    <p>Os preços e a disponibilidade podem mudar no site do vendedor.</p>
    <p>© 2026 - OS ACHADOS</p>
</div>
""", unsafe_allow_html=True)
