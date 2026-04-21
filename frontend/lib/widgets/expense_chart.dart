import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class ExpenseChart extends StatelessWidget {
  const ExpenseChart({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 200,
      child: LineChart(
        LineChartData(
          gridData: FlGridData(show: false),
          titlesData: FlTitlesData(show: false),
          borderData: FlBorderData(show: false),

          lineBarsData: [
            LineChartBarData(
              isCurved: true,
              color: const Color(0xFFD4AF37),
              barWidth: 3,
              spots: const [
                FlSpot(0, 200),
                FlSpot(1, 500),
                FlSpot(2, 300),
                FlSpot(3, 700),
                FlSpot(4, 400),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
