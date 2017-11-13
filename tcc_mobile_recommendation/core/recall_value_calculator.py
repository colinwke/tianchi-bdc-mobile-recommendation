"""
线上提交结果recall值及正确数计算
"""

value = "10.00000000% 0.09942639"

preferenceSet = 517

fscore = float(value.split(sep='% ')[0])
precision = float(value.split(sep='% ')[1])

recall = (fscore * precision / 100) / (2 * precision - fscore / 100)

tp = round(preferenceSet * recall)
predictionSet = round(tp / precision)

print("%.8f%% %.8f %.8f %.0f %.0f" % (fscore, precision, recall, tp, predictionSet))
