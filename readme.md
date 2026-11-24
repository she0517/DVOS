Other scripts will be uploaded to the repository later...

an example:

> closing the GUI interface will result in faster solving speed...

<img width="1102" height="765" alt="image" src="https://github.com/user-attachments/assets/44d0028a-462e-40a0-a5a8-b097db4f6b2c" />

<img width="868" height="445" alt="MP_solver_迭代过程" src="https://github.com/user-attachments/assets/be17505a-2128-4bbc-94ea-8d0d3c457567" />

```
>>colonnade' Engine has been built successfully
>>Engine(name='MP_solver') configuration information 
[1]ToolBox contains tools: buildRestrictedMP, generateInitialCols, updateAndSolveSP_Exact, updateAndSolveSP_Heuristic
[2]Environment(
    ├── (parameter  1) variables_name               : 'labda'
    ├── (parameter  2) relaxed_variables_name       : ['labda']
    ├── (parameter  3) relaxed_variables_type       : ['BINARY']
    ├── (parameter  4) fingerprint_lst              : [(3, 3), (8, 3), (3, 2), (9, 3), (15, 2)]
                                                      (...+26 more, total=31)
    ├── (parameter  5) barrier_method_on            : True
    ├── (parameter  6) exact_solve_on               : True
    ├── (parameter  7) heuristic_solve_on           : True
    ├── (parameter  8) sps_parallel_on              : False
    ├── (parameter  9) process_num                  : None
    ├── (parameter 10) mini_batch_percent           : 0.1
    ├── (parameter 11) lp_file_ouput_on             : False
    ├── (parameter 12) ilp_file_output_on           : True
    ├── (parameter 13) col_file_output_on           : False
    ├── (parameter 14) result_file_output_on        : False
    ├── (parameter 15) result_gui_on                : True
    ├── (parameter 16) dual_alpha                   : 0
    ├── (parameter 17) truncate_threshold           : 0.001
    ├── (parameter 18) max_not_better               : 10
    ├── (parameter 19) innocent                     : 50
    ├── (parameter 20) max_column_num               : inf
    ├── (parameter 21) max_time_limit               : 3600
    ├── (parameter 22) rmp_log_to_console           : False
    ├── (parameter 23) current_reduced_cost_on      : False
    └── (parameter 24) in_rmp_optimal_basis_when_on : False
)

>>Note:在调用runEngine前请先检查配置是否满足你的要求

>>预备：初始列构造完毕
Cardinal Optimizer v8.0.6. Build date Aug  7 2026
Copyright Cardinal Operations 2026. All Rights Reserved

>>限制主问题数学模型构造完毕，进入列生成迭代轮次

>>列生成迭代过程：
+-----+---------+---------+--------------+----------+------------+------------+------------+
|iter |time(s)  |cols_num |rmp_obj       |no_better |rmp_time(s) |sps_method  |sps_time(s) |
+-----+---------+---------+--------------+----------+------------+------------+------------+
|1    |0.24     |15       |3,262.00      |-1        |0.00        |heuristic   |0.21        |
|2    |0.38     |18       |3,262.00      |-1        |0.00        |heuristic   |0.11        |
|3    |0.43     |21       |3,262.00      |-1        |0.00        |heuristic   |0.02        |
|4    |0.48     |24       |3,262.00      |-1        |0.00        |heuristic   |0.01        |
|5    |0.63     |27       |3,262.00      |-1        |0.00        |heuristic   |0.11        |
|6    |0.67     |30       |3,262.00      |-1        |0.00        |heuristic   |0.01        |
|7    |0.72     |33       |3,262.00      |-1        |0.00        |heuristic   |0.01        |
|8    |0.76     |36       |3,262.00      |-1        |0.00        |heuristic   |0.01        |
|9    |0.93     |39       |3,262.00      |-1        |0.00        |heuristic   |0.13        |
|10   |1.00     |42       |3,262.00      |-1        |0.00        |heuristic   |0.01        |
|11   |1.08     |45       |3,262.00      |-1        |0.00        |heuristic   |0.01        |
|12   |1.18     |48       |3,262.00      |-1        |0.00        |heuristic   |0.06        |
|13   |1.23     |51       |3,262.00      |-1        |0.00        |heuristic   |0.02        |
|14   |1.70     |54       |3,262.00      |-1        |0.00        |heuristic   |0.42        |
|15   |1.78     |57       |3,262.00      |-1        |0.00        |heuristic   |0.03        |
|16   |1.86     |60       |3,262.00      |-1        |0.01        |heuristic   |0.01        |
|17   |1.93     |63       |3,262.00      |-1        |0.02        |heuristic   |0.01        |
|18   |2.01     |66       |3,262.00      |-1        |0.01        |heuristic   |0.04        |
|19   |2.07     |69       |3,262.00      |-1        |0.01        |heuristic   |0.01        |
|20   |2.13     |72       |3,134.89      |-1        |0.01        |heuristic   |0.01        |
|21   |2.19     |75       |3,093.73      |-1        |0.01        |heuristic   |0.01        |
|22   |2.26     |78       |3,011.61      |-1        |0.01        |heuristic   |0.01        |
|23   |2.32     |81       |3,009.27      |-1        |0.01        |heuristic   |0.01        |
|24   |2.38     |84       |3,007.07      |-1        |0.01        |heuristic   |0.01        |
|25   |2.56     |87       |2,983.44      |-1        |0.01        |heuristic   |0.13        |
|26   |2.64     |90       |2,940.78      |-1        |0.01        |heuristic   |0.02        |
|27   |2.70     |93       |2,918.83      |-1        |0.02        |heuristic   |0.01        |
|28   |2.77     |96       |2,900.19      |-1        |0.02        |heuristic   |0.02        |
|29   |2.83     |99       |2,868.36      |-1        |0.02        |heuristic   |0.01        |
|30   |2.90     |102      |2,844.44      |-1        |0.03        |heuristic   |0.01        |
|31   |2.99     |105      |2,801.84      |-1        |0.03        |heuristic   |0.02        |
|32   |3.07     |108      |2,801.45      |-1        |0.03        |heuristic   |0.02        |
|33   |3.18     |111      |2,795.27      |-1        |0.03        |heuristic   |0.03        |
|34   |3.29     |114      |2,781.23      |-1        |0.03        |heuristic   |0.03        |
|35   |3.47     |117      |2,759.02      |-1        |0.03        |heuristic   |0.10        |
|36   |3.57     |120      |2,685.17      |-1        |0.04        |heuristic   |0.03        |
|37   |3.74     |123      |2,682.09      |-1        |0.03        |heuristic   |0.09        |
|38   |3.83     |126      |2,675.80      |-1        |0.03        |heuristic   |0.02        |
|39   |3.93     |129      |2,660.18      |-1        |0.04        |heuristic   |0.02        |
|40   |4.04     |132      |2,657.73      |-1        |0.04        |heuristic   |0.03        |
|41   |4.16     |135      |2,652.70      |-1        |0.03        |heuristic   |0.04        |
|42   |4.29     |138      |2,636.41      |-1        |0.04        |heuristic   |0.04        |
|43   |4.43     |141      |2,636.41      |-1        |0.05        |heuristic   |0.06        |
|44   |4.55     |144      |2,600.83      |-1        |0.04        |heuristic   |0.03        |
|45   |4.64     |147      |2,594.86      |-1        |0.04        |heuristic   |0.02        |
|46   |4.78     |150      |2,588.50      |-1        |0.04        |heuristic   |0.07        |
|47   |4.90     |153      |2,579.21      |-1        |0.05        |heuristic   |0.02        |
|48   |4.99     |156      |2,577.82      |-1        |0.04        |heuristic   |0.02        |
|49   |5.12     |159      |2,572.89      |-1        |0.04        |heuristic   |0.05        |
|50   |5.24     |162      |2,570.81      |-1        |0.05        |heuristic   |0.03        |
|51   |5.33     |165      |2,570.35      |0         |0.04        |heuristic   |0.03        |
|52   |5.67     |168      |2,566.03      |0         |0.06        |heuristic   |0.23        |
|53   |5.87     |171      |2,558.09      |0         |0.05        |heuristic   |0.09        |
|54   |6.00     |174      |2,558.07      |0         |0.04        |heuristic   |0.04        |
|55   |6.25     |177      |2,554.16      |0         |0.05        |heuristic   |0.17        |
|56   |6.62     |180      |2,549.72      |0         |0.07        |heuristic   |0.26        |
|57   |6.78     |183      |2,549.72      |1         |0.06        |heuristic   |0.05        |
|58   |7.01     |186      |2,543.40      |0         |0.06        |heuristic   |0.13        |
|59   |7.18     |189      |2,543.20      |0         |0.05        |heuristic   |0.06        |
|60   |7.46     |192      |2,543.20      |0         |0.08        |heuristic   |0.15        |
|61   |7.66     |195      |2,542.43      |0         |0.05        |heuristic   |0.11        |
|62   |7.80     |198      |2,542.30      |0         |0.06        |heuristic   |0.04        |
|63   |7.97     |201      |2,542.30      |1         |0.06        |heuristic   |0.06        |
|64   |8.11     |204      |2,540.94      |0         |0.05        |heuristic   |0.05        |
|65   |8.26     |207      |2,540.33      |0         |0.05        |heuristic   |0.05        |
|66   |8.47     |210      |2,536.50      |0         |0.05        |heuristic   |0.12        |
|67   |8.77     |213      |2,536.50      |1         |0.05        |heuristic   |0.21        |
|68   |8.88     |216      |2,535.53      |0         |0.05        |heuristic   |0.03        |
|69   |9.09     |219      |2,535.17      |0         |0.05        |heuristic   |0.13        |
|70   |9.42     |222      |2,533.42      |0         |0.05        |heuristic   |0.24        |
|71   |9.63     |225      |2,533.25      |0         |0.05        |heuristic   |0.12        |
|72   |9.83     |228      |2,533.25      |1         |0.07        |heuristic   |0.11        |
|73   |9.99     |231      |2,532.33      |0         |0.05        |heuristic   |0.07        |
|74   |10.33    |234      |2,532.33      |1         |0.05        |heuristic   |0.25        |
|75   |10.56    |237      |2,531.50      |0         |0.06        |heuristic   |0.14        |
|76   |10.81    |240      |2,523.51      |0         |0.08        |heuristic   |0.13        |
|77   |11.01    |243      |2,523.51      |1         |0.06        |heuristic   |0.10        |
|78   |11.21    |246      |2,523.50      |0         |0.08        |heuristic   |0.06        |
|79   |11.57    |249      |2,519.09      |0         |0.07        |heuristic   |0.23        |
|80   |11.97    |252      |2,516.36      |0         |0.06        |heuristic   |0.31        |
|81   |12.17    |255      |2,516.36      |1         |0.06        |heuristic   |0.09        |
|82   |12.45    |258      |2,513.98      |0         |0.06        |heuristic   |0.19        |
|83   |12.78    |261      |2,513.84      |0         |0.06        |heuristic   |0.25        |
|84   |13.32    |264      |2,513.06      |0         |0.06        |heuristic   |0.44        |
|85   |13.61    |267      |2,513.05      |0         |0.06        |heuristic   |0.19        |
|86   |13.88    |270      |2,513.05      |1         |0.07        |heuristic   |0.15        |
|87   |14.45    |273      |2,513.05      |2         |0.07        |heuristic   |0.46        |
|88   |14.96    |276      |2,512.41      |0         |0.08        |heuristic   |0.38        |
|89   |15.57    |279      |2,512.02      |0         |0.09        |heuristic   |0.47        |
|90   |16.21    |282      |2,511.98      |0         |0.08        |heuristic   |0.52        |
|91   |16.49    |285      |2,511.65      |0         |0.08        |heuristic   |0.15        |
|92   |17.26    |288      |2,511.65      |1         |0.09        |heuristic   |0.64        |
|93   |17.83    |291      |2,511.38      |0         |0.07        |heuristic   |0.45        |
|94   |18.23    |294      |2,511.38      |1         |0.08        |heuristic   |0.27        |
|95   |19.03    |297      |2,511.32      |0         |0.08        |heuristic   |0.67        |
|96   |19.87    |300      |2,510.50      |0         |0.09        |heuristic   |0.71        |
|97   |20.12    |303      |2,510.50      |1         |0.08        |heuristic   |0.13        |
|98   |21.52    |306      |2,510.50      |2         |0.08        |heuristic   |1.27        |
|99   |22.00    |309      |2,510.50      |3         |0.08        |heuristic   |0.36        |
|100  |22.57    |312      |2,510.50      |4         |0.08        |heuristic   |0.44        |
|101  |22.86    |315      |2,510.13      |0         |0.08        |heuristic   |0.17        |
|102  |23.57    |318      |2,510.12      |1         |0.08        |heuristic   |0.58        |
|103  |24.92    |321      |2,510.00      |0         |0.09        |heuristic   |1.22        |
|104  |26.68    |324      |2,510.00      |1         |0.14        |heuristic   |1.57        |
|105  |28.62    |327      |2,510.00      |2         |0.08        |heuristic   |1.80        |
|106  |30.12    |330      |2,510.00      |3         |0.09        |heuristic   |1.35        |
|107  |31.57    |333      |2,510.00      |4         |0.08        |heuristic   |1.34        |
|108  |33.19    |336      |2,510.00      |5         |0.08        |heuristic   |1.51        |
|109  |35.35    |339      |2,510.00      |6         |0.09        |heuristic   |2.04        |
|110  |36.40    |342      |2,510.00      |7         |0.07        |heuristic   |0.95        |
|111  |38.24    |345      |2,510.00      |8         |0.08        |heuristic   |1.73        |
|112  |39.42    |348      |2,510.00      |9         |0.08        |heuristic   |1.07        |
|113  |42.12    |351      |2,509.50      |0         |0.08        |heuristic   |2.58        |
|114  |45.76    |354      |2,509.50      |1         |0.08        |heuristic   |3.54        |
|115  |49.05    |356      |2,509.50      |2         |0.08        |heuristic   |3.16        |
|116  |53.06    |358      |2,509.50      |3         |0.08        |heuristic   |3.90        |
|117  |62.61    |358      |2,509.50      |4         |0.08        |exact       |9.44        |
|118  |62.92    |360      |2,509.50      |5         |0.10        |exact       |0.17        |
|119  |64.22    |363      |2,509.50      |6         |0.09        |exact       |1.17        |
|120  |65.30    |366      |2,509.50      |7         |0.10        |exact       |0.93        |
|121  |65.94    |369      |2,509.50      |8         |0.08        |exact       |0.52        |
|122  |66.77    |372      |2,509.50      |9         |0.09        |exact       |0.71        |
|123  |68.38    |375      |2,509.50      |10        |0.10        |exact       |1.49        |
+-----+---------+---------+--------------+----------+------------+------------+------------+
>>列生成迭代终止原因：达到最大容许未改进次数max_not_better
>>列生成迭代轮次终止，下面将根据现有ColumnPool对主问题进行求解：

Setting parameter 'Logging' to 1
Setting parameter 'LpMethod' to -1
Setting parameter 'BarHomogeneous' to -1
Setting parameter 'Scaling' to -1
Model fingerprint: ad7553e1

Using Cardinal Optimizer v8.0.6 on Windows (26H2 Build 26300 - x86_64)
The CPU model is 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
Hardware has 4 physical cores and 8 logical cores. Using instruction set X86_AVX512_E1 (14)
Minimizing a MIP problem

The original problem has:
    6495 rows, 378 columns and 42403 non-zero elements
    378 binaries

Starting the MIP solver with 8 threads and 32 tasks

Presolving the problem

The presolved problem has:
    435 rows, 371 columns and 7615 non-zero elements
    371 binaries

Problem info:
    Range of matrix coefficients:    [1e+00,2e+04]
    Range of rhs coefficients:       [1e+00,2e+04]
    Range of bound coefficients:     [1e+00,1e+00]
    Range of cost coefficients:      [3e+01,1e+03]
    Density of cost:                     100.0%

     Nodes    Active  LPit/n  IntInf     BestBound  BestSolution     Gap   Time
         0         1      --       0  0.000000e+00            --     Inf  0.17s
H        0         1      --       0  0.000000e+00  3.262000e+03 100.00%  0.18s
         0         1      --      39  2.515500e+03  3.262000e+03  22.88%  0.25s
H        0         1      --      39  2.515500e+03  2.834000e+03  11.24%  0.33s
         0         1      --      39  2.515500e+03  2.834000e+03  11.24%  0.33s
         0         1      --      44  2.516625e+03  2.834000e+03  11.20%  0.36s
         0         1      --      46  2.516825e+03  2.834000e+03  11.19%  0.37s
         0         1      --      37  2.518750e+03  2.834000e+03  11.12%  0.38s
         0         1      --      41  2.518786e+03  2.834000e+03  11.12%  0.39s
         0         1      --      46  2.518821e+03  2.834000e+03  11.12%  0.39s
         0         1      --      28  2.521833e+03  2.834000e+03  11.02%  0.40s
         0         1      --      44  2.522320e+03  2.834000e+03  11.00%  0.41s
*        0         1      --       0  2.525000e+03  2.525000e+03  0.000%  0.42s
         0         1      --       0  2.525000e+03  2.525000e+03  0.000%  0.42s
         1         0   145.0       0  2.525000e+03  2.525000e+03  0.000%  0.42s

     Nodes    Active  LPit/n  IntInf     BestBound  BestSolution     Gap   Time
         1         0   145.0       0  2.525000e+03  2.525000e+03  0.000%  0.42s

Best solution   : 2525.000000000
Best bound      : 2525.000000000
Best gap        : 0.0000%
Solve time      : 0.42
Solve node      : 1
MIP status      : solved
Solution status : integer optimal (relative gap limit 0.0001)

Violations      :     absolute     relative
    bounds      :  2.66454e-15  2.66454e-15
    rows        :  2.66454e-15  2.66454e-15
    integrality :  2.66454e-15
MP模型的最优解对应的列：[<colonnade.utils.Column object at 0x000002A58939FBE0>, <colonnade.utils.Column object at 0x000002A589560940>, <colonnade.utils.Column object at 0x000002A589561C60>, <colonnade.utils.Column object at 0x000002A5895630A0>, <colonnade.utils.Column object at 0x000002A589563B80>, <colonnade.utils.Column object at 0x000002A58C32D000>, <colonnade.utils.Column object at 0x000002A58C32CDC0>, <colonnade.utils.Column object at 0x000002A58C32D120>, <colonnade.utils.Column object at 0x000002A58C32EB60>, <colonnade.utils.Column object at 0x000002A58C32DA80>, <colonnade.utils.Column object at 0x000002A58C32F4C0>, <colonnade.utils.Column object at 0x000002A58C32F520>, <colonnade.utils.Column object at 0x000002A58C32EFE0>, <colonnade.utils.Column object at 0x000002A58C32F6A0>, <colonnade.utils.Column object at 0x000002A5891D4460>]
MP模型求解时列池中列的数量：378
MP模型的最优值：2525.0000000000005
RMP模型最后一次迭代的最优值：2509.5
总求解时长：68.8280394077301秒
```
