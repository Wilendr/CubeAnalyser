import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import os

matplotlib.rcParams['font.family'] = 'monospace'

def plot_timecourse(archetypes, storage_matrix, window, save_folder='results'):

    '''Given a dataframe containing time course information, plot the win rates'''
    fig, ax = plt.subplots(1,1, figsize = (10,6))

    # only does this for the super archetypes (Aggro, Midrange, Control). Other archetypes are too infrequent to get a good picture.
    colors = {'Aggro':'#ffa600', 'Midrange':'#bc5090', 'Control':'#003f5c'}
    for i, archetype in enumerate(archetypes):
        if archetype in ['Aggro', 'Midrange', 'Control']:
            data = storage_matrix[i, :]
            ax.plot(range(len(data)), data, label='{}'.format(archetype), color=colors.get(archetype, 'black'))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.legend(fontsize = 14)
    plt.xlabel('Decks', fontsize = 18)
    plt.ylabel('Rolling Average', fontsize = 18)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.title(f'Archetype Winrates, Window={window}', fontsize = 18)
    plt.tight_layout()

    fig.savefig(os.path.join(save_folder, 'Archetype_Winrates.png'), dpi = 300)
    plt.close(fig)

def plot_color_curve(num_colors, save_folder='results'):

    fig, ax = plt.subplots(1,1, figsize = (10,6))

    ax.bar(list(num_colors.keys()), list(num_colors.values()))

    for i in range(len(list(num_colors.keys()))):
        plt.text(i, list(num_colors.values())[i] + 0.005, round(list(num_colors.values())[i], 2), ha = 'center')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.ylim(0, round(max(list(num_colors.values())), 1) + 0.05)
    plt.ylabel('Decks %', fontsize = 18)
    plt.xticks(fontsize = 10)
    plt.xticks(rotation=45)
    plt.yticks(fontsize = 14)
    plt.title(f'Number of Colors', fontsize = 18)
    plt.tight_layout()

    fig.savefig(os.path.join(save_folder, 'Color_Curve.png'), dpi = 300)
    plt.close(fig)


def plot_archetype_analysis(save_folder='results'):
    fig, ax = plt.subplots()

    ax.axis('off')
    ax.axis('tight')

    df = pd.read_csv(os.path.join(save_folder, 'csv-files/Archetype_Analysis.csv'))
    df = df.round(3).sort_values(by='Win %', ascending=False)
    df_limited = df.head(20)

    table = ax.table(cellText=df_limited.values, colLabels=df_limited.columns, loc='center', cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(7)

    plt.title('Archetype Analysis')

    fig.tight_layout()

    fig.savefig(os.path.join(save_folder, 'Archetype_Analysis.png'), dpi = 300)
    plt.close(fig)


def plot_card_win_analysis(save_folder='results'):
    fig, ax = plt.subplots()

    ax.axis('off')
    ax.axis('tight')

    df = pd.read_csv(os.path.join(save_folder, 'csv-files/Card_Analysis_Win%.csv'))
    df = df.round(3).drop(columns=['Num', 'Color', 'Mana Value', 'Type'])
    df.insert(0, 'Rank', range(1, len(df) + 1))
    df_limited = pd.concat([df.head(10), df.tail(10)])

    dots_row = pd.DataFrame([['...','...','...','...', '...', '...', '...']], columns=df_limited.columns)
    df_limited_before = df_limited.iloc[:10]
    df_limited_after = df_limited.iloc[10:]

    df_final = pd.concat([df_limited_before, dots_row, df_limited_after], ignore_index=True)

    table = ax.table(cellText=df_final.values, colLabels=df_final.columns, loc='center', cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(7)

    col_width = max(len(str(val)) for val in df_final[df_final.columns[1]])
    for key, cell in table.get_celld().items():
        if key[1] == 1:
            cell.set_width(col_width*0.0125)

    plt.title('Top 10 & Bottom 10 Win %')

    fig.tight_layout()
    fig.savefig(os.path.join(save_folder, 'Card_Analysis_Win%.png'), dpi = 300)
    plt.close(fig)


def plot_card_main_analysis(save_folder='results'):
    fig, ax = plt.subplots()

    ax.axis('off')
    ax.axis('tight')

    df = pd.read_csv(os.path.join(save_folder, 'csv-files/Card_Analysis_Main%.csv'))
    df = df.round(3).drop(columns=['Num', 'Color', 'Mana Value', 'Type'])
    df.insert(0, 'Rank', range(1, len(df) + 1))
    df_limited = pd.concat([df.head(10), df.tail(10)])

    dots_row = pd.DataFrame([['...','...','...','...', '...', '...', '...']], columns=df_limited.columns)
    df_limited_before = df_limited.iloc[:10]
    df_limited_after = df_limited.iloc[10:]

    df_final = pd.concat([df_limited_before, dots_row, df_limited_after], ignore_index=True)


    table = ax.table(cellText=df_final.values, colLabels=df_final.columns, loc='center', cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(7)

    col_width = max(len(str(val)) for val in df_final[df_final.columns[1]])
    for key, cell in table.get_celld().items():
        if key[1] == 1:
            cell.set_width(col_width*0.0125)

    plt.title('Top 10 & Bottom 10 Main %')

    fig.tight_layout()
    fig.savefig(os.path.join(save_folder, 'Card_Analysis_Main%.png'), dpi = 300)
    plt.close(fig)


def plot_card_norm_analysis(save_folder='results'):
    fig, ax = plt.subplots()

    ax.axis('off')
    ax.axis('tight')

    df = pd.read_csv(os.path.join(save_folder, 'csv-files/Card_Analysis_Norm%.csv'))
    df = df.round(3).drop(columns=['Num', 'Color', 'Mana Value', 'Type'])
    df.insert(0, 'Rank', range(1, len(df) + 1))
    df_limited = pd.concat([df.head(10), df.tail(10)])

    dots_row = pd.DataFrame([['...','...','...','...', '...', '...', '...']], columns=df_limited.columns)
    df_limited_before = df_limited.iloc[:10]
    df_limited_after = df_limited.iloc[10:]

    df_final = pd.concat([df_limited_before, dots_row, df_limited_after], ignore_index=True)

    table = ax.table(cellText=df_final.values, colLabels=df_final.columns, loc='center', cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(7)

    col_width = max(len(str(val)) for val in df_final[df_final.columns[1]])
    for key, cell in table.get_celld().items():
        if key[1] == 1:
            cell.set_width(col_width*0.0125)

    plt.title('Top 10 & Bottom 10 Norm %')

    fig.tight_layout()
    fig.savefig(os.path.join(save_folder, 'Card_Analysis_Norm%.png'), dpi = 300)
    plt.close(fig)


def plot_color_analysis(save_folder='results'):
    fig, ax = plt.subplots(figsize=(6, 2.25))

    ax.axis('off')
    ax.axis('tight')

    df = pd.read_csv(os.path.join(save_folder, 'csv-files/Color_Analysis.csv'))
    df = df.round(3)

    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

    row_height = 0.15
    for key, cell in table.get_celld().items():
        cell.set_height(row_height)
    
    table.auto_set_font_size(False)
    table.set_fontsize(7)

    plt.title('Color Analysis')

    fig.tight_layout()
    fig.savefig(os.path.join(save_folder, 'Color_Analysis.png'), dpi = 300)
    plt.close(fig)


def plot_player_analysis(save_folder='results'):
    fig, ax = plt.subplots(figsize=(6,3.5))

    ax.axis('off')
    ax.axis('tight')

    df = pd.read_csv(os.path.join(save_folder, 'csv-files/Player_Analysis.csv'))
    df = df.round(3).sort_values(by='Win %', ascending=False)
    df = df.loc[df['Num'] >= 3]
    df.insert(0, 'Rank', range(1, len(df) + 1))
    df_limited = df.head(10)

    table = ax.table(cellText=df_limited.values, colLabels=df_limited.columns, loc='center', cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(7)

    row_height = 0.085
    for key, cell in table.get_celld().items():
        cell.set_height(row_height)

    col_width = max(len(str(val)) for val in df_limited[df_limited.columns[1]])
    for key, cell in table.get_celld().items():
        if key[1] == 1:
            cell.set_width(col_width*0.0125)

    plt.title('Top 10 Players')

    fig.tight_layout()
    fig.savefig(os.path.join(save_folder, 'Player_Analysis.png'), dpi = 300)
    plt.close(fig)