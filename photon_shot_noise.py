import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const NoisyPoissonHistogram = () => {
  const [data, setData] = useState([]);
  const lambda = 3;  // Changed to 3
  const noiseSigma = 0.1;
  const sampleSize = 10000;
  const binSize = 0.05;
  const maxK = 10;  // Increased to account for higher lambda

  // Box-Muller transform for generating Gaussian noise
  const gaussianRandom = () => {
    let u = 0, v = 0;
    while(u === 0) u = Math.random();
    while(v === 0) v = Math.random();
    return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
  };

  const poissonSample = () => {
    let L = Math.exp(-lambda);
    let k = 0;
    let p = 1;
    do {
      k++;
      p *= Math.random();
    } while (p > L);
    return k - 1;
  };

  const addNoise = (k) => {
    return Math.max(0, k + gaussianRandom() * noiseSigma);
  };

  const generateHistogramData = (samples) => {
    const histogramData = {};
    const maxBin = Math.ceil(maxK / binSize) * binSize;

    for (let i = 0; i <= maxBin; i += binSize) {
      histogramData[i.toFixed(2)] = 0;
    }

    samples.forEach(sample => {
      const bin = (Math.floor(sample / binSize) * binSize).toFixed(2);
      if (bin in histogramData) {
        histogramData[bin]++;
      }
    });

    return Object.entries(histogramData).map(([bin, count]) => ({
      bin: parseFloat(bin),
      count: count / sampleSize // Normalize to get proportions
    }));
  };

  useEffect(() => {
    const samples = Array(sampleSize).fill().map(() => addNoise(poissonSample()));
    const histogramData = generateHistogramData(samples);
    setData(histogramData);
  }, []);

  return (
    <div className="w-full h-96 p-4">
      <h2 className="text-xl font-bold mb-4">Poisson Distribution (λ = 3) with Low Gaussian Noise (σ = 0.1, 10000 samples, bin size 0.05)</h2>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="bin" 
            label={{ value: 'Noisy Event Count', position: 'insideBottom', offset: -5 }} 
            domain={[0, maxK]}
            ticks={Array.from({length: maxK + 1}, (_, i) => i)}
          />
          <YAxis 
            label={{ value: 'Proportion', angle: -90, position: 'insideLeft' }}
            domain={[0, 'auto']}
          />
          <Tooltip 
            formatter={(value, name, props) => [value.toFixed(5), 'Proportion']}
            labelFormatter={(value) => `Bin: ${value.toFixed(2)} - ${(value + binSize).toFixed(2)}`}
          />
          <Legend />
          <Bar dataKey="count" fill="#8884d8" name="Proportion" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default NoisyPoissonHistogram;
