'''
统计标注类别和各类别数量
2020.4.21
'''
import operator
import sys
import argparse
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

path = 'D:\wsm\pycharm_pjs\data-analysis\scripts\\traffic_anno.txt'  #标注txt文件路径
results_files_path = 'D:\wsm\pycharm_pjs\data-analysis\scripts\\' #结果输出位置
image_num = 13910   #手动输入图片数量#由selfimage_annotation.py输出得到
draw_plot = True
gt_counter_per_class = {}

'''
从txt统计类别信息到字典gt_counter_per_class
'''
with open(path,'r') as f:
    for line in f.readlines():
        class_list = line.strip().split(',')[1:]
        print(class_list)
        for class_name in class_list:
            if class_name in gt_counter_per_class:
                gt_counter_per_class[class_name] += 1
            else:
                gt_counter_per_class[class_name] = 1
print(gt_counter_per_class)

# 类别列表、类别数
gt_classes = list(gt_counter_per_class.keys())
#print(gt_classes)
n_classes = len(gt_classes)


"""
 Plot - adjust axes
"""
def adjust_axes(r, t, fig, axes):
  # get text width for re-scaling
  bb = t.get_window_extent(renderer=r)
  text_width_inches = bb.width / fig.dpi
  # get axis width in inches
  current_fig_width = fig.get_figwidth()
  new_fig_width = current_fig_width + text_width_inches
  propotion = new_fig_width / current_fig_width
  # get axis limit
  x_lim = axes.get_xlim()
  axes.set_xlim([x_lim[0], x_lim[1]*propotion])

"""
 Draw plot using Matplotlib
"""
def draw_plot_func(dictionary, n_classes, window_title, plot_title, x_label, output_path, to_show, plot_color, true_p_bar):
  # sort the dictionary by decreasing value, into a list of tuples
  sorted_dic_by_value = sorted(dictionary.items(), key=operator.itemgetter(1))
  # unpacking the list of tuples into two lists
  sorted_keys, sorted_values = zip(*sorted_dic_by_value)
  #
  if true_p_bar != "":
    """
     Special case to draw in (green=true predictions) & (red=false predictions)
    """
    fp_sorted = []
    tp_sorted = []
    for key in sorted_keys:
      fp_sorted.append(dictionary[key] - true_p_bar[key])
      tp_sorted.append(true_p_bar[key])
    plt.barh(range(n_classes), fp_sorted, align='center', color='crimson', label='False Predictions')
    plt.barh(range(n_classes), tp_sorted, align='center', color='forestgreen', label='True Predictions', left=fp_sorted)
    # add legend
    plt.legend(loc='lower right')
    """
     Write number on side of bar
    """
    fig = plt.gcf() # gcf - get current figure
    axes = plt.gca()
    r = fig.canvas.get_renderer()
    for i, val in enumerate(sorted_values):
      fp_val = fp_sorted[i]
      tp_val = tp_sorted[i]
      fp_str_val = " " + str(fp_val)
      tp_str_val = fp_str_val + " " + str(tp_val)
      # trick to paint multicolor with offset:
      #   first paint everything and then repaint the first number
      t = plt.text(val, i, tp_str_val, color='forestgreen', va='center', fontweight='bold')
      plt.text(val, i, fp_str_val, color='crimson', va='center', fontweight='bold')
      if i == (len(sorted_values)-1): # largest bar
        adjust_axes(r, t, fig, axes)
  else:
    plt.barh(range(n_classes), sorted_values, color=plot_color)
    """
     Write number on side of bar
    """
    fig = plt.gcf() # gcf - get current figure
    axes = plt.gca()
    r = fig.canvas.get_renderer()
    for i, val in enumerate(sorted_values):
      str_val = " " + str(val) # add a space before
      if val < 1.0:
        str_val = " {0:.2f}".format(val)
      t = plt.text(val, i, str_val, color=plot_color, va='center', fontweight='bold')
      # re-set axes to show number inside the figure
      if i == (len(sorted_values)-1): # largest bar
        adjust_axes(r, t, fig, axes)
  # set window title
  fig.canvas.set_window_title(window_title)
  # write classes in y axis
  tick_font_size = 12
  plt.yticks(range(n_classes), sorted_keys, fontsize=tick_font_size)
  """
   Re-scale height accordingly
  """
  init_height = fig.get_figheight()
  # comput the matrix height in points and inches
  dpi = fig.dpi
  height_pt = n_classes * (tick_font_size * 1.4) # 1.4 (some spacing)
  height_in = height_pt / dpi
  # compute the required figure height
  top_margin = 0.15    # in percentage of the figure height
  bottom_margin = 0.05 # in percentage of the figure height
  figure_height = height_in / (1 - top_margin - bottom_margin)
  # set new height
  if figure_height > init_height:
    fig.set_figheight(figure_height)

  # set plot title
  plt.title(plot_title, fontsize=14)
  # set axis titles
  # plt.xlabel('classes')
  plt.xlabel(x_label, fontsize='large')
  # adjust size of window
  fig.tight_layout()
  # save the plot
  fig.savefig(output_path)
  # show image
  if to_show:
    plt.show()
  # close the plot
  plt.close()


"""
 Plot the total number of occurences of each class in the ground-truth
"""
if draw_plot:
  true_p_bar = gt_counter_per_class
  window_title = "Ground-Truth Info"
  plot_title = "Ground-Truth\n"
  plot_title += "(" + str(image_num) + " pictures and " + str(n_classes) + " classes)"
  x_label = "Number of objects per class"
  output_path = results_files_path + "/traffic_anno Ground-Truth Info.png"
  to_show = False
  plot_color = 'forestgreen'
  draw_plot_func(
    gt_counter_per_class,
    n_classes,
    window_title,
    plot_title,
    x_label,
    output_path,
    to_show,
    plot_color,
    '',
    )