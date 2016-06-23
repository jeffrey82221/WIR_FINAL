import matplotlib.pylab as plt
def plot_np_matrix(M):
    import matplotlib.pylab as plt
    import numpy as np
    np.fill_diagonal(M, 0.)
    plt.imshow(M,interpolation='nearest')
    plt.colorbar()

def plot_matrix(table):
    import matplotlib.pyplot as plt
    import numpy as np
    M = np.matrix(table)
    (W,H) = np.shape(M)
    if(W==H):
        np.fill_diagonal(M, 0.)
    plt.imshow(M,interpolation='nearest')
    plt.colorbar()
    tick_marks_x = np.arange(len(list(table.columns)))
    tick_marks_y = np.arange(len(list(table.index)))
    plt.xticks(tick_marks_x, list(table.columns), rotation=45)
    plt.yticks(tick_marks_y, list(table.index))
    plt.show()



def compare_table_values(table1,table2):
    import matplotlib.pylab as plt
    import numpy as np
    (W,L) = np.shape(np.matrix(table1))
    plt.scatter(np.reshape(np.matrix(table1),(W*L,1)),np.reshape(np.matrix(table2),(W*L,1)))
    plt.show()

def dimension_reduction(table):
    from sklearn.manifold import TSNE
    import numpy as np
    import pandas as pd
    tsne = TSNE(n_components=int(2), perplexity=30.0, early_exaggeration=10.0,
                learning_rate=1000.0,  n_iter=3000, metric='euclidean', init='pca')
    result = tsne.fit_transform(np.matrix(table))
    return pd.DataFrame(result, index=table.index)


def plot_word_embedding(plt, table, labels=None, title='', num=1):
    import numpy as np
    plt.figure(num)
    vectors = np.matrix(table).tolist()
    words = list(table.index)

    import matplotlib
    if(type(labels) == type(None)):
        None
        colors = None
    else:
        label_set = list(set(list(labels.values.transpose().tolist())[0]))

        def get_spaced_colors(n):
            max_value = 16581375  # 255**3
            interval = int(max_value / n)
            colors = [hex(I)[2:].zfill(6)
                      for I in range(0, max_value, interval)]

            return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]
        colors = get_spaced_colors(len(label_set))

    for i in range(len(words)):
        point = vectors[i]
        word = words[i]
        # plot points
        plt.scatter(point[0], point[1])
        # plot word annotations
        if(type(labels) == type(None)):

            plt.annotate(
                word,
                xy=(point[0], point[1]),
                size="x-small"
            )
        else:
            label_index = label_set.index(
                list(labels.values.transpose().tolist())[0][i])
            plt.annotate(
                word,
                xy=(point[0], point[1]),
                color='#' +
                "".join(list(map(lambda x: format(x, '#04x')
                                 [2:], colors[label_index]))).upper(),
                size="x-small"
            )

    plt.tight_layout()
    plt.title(title)
