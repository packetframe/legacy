package main

import (
	"context"
	"flag"
	"github.com/go-ping/ping"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	log "github.com/sirupsen/logrus"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"net/http"
	"os"
	"time"
)

const updateDelay = 10 * time.Second

var (
	listenAddr = flag.String("web.listen-addr", ":9786", "Listening Address")
	mongoAddr  = flag.String("db", "mongodb://localhost:27017", "MongoDB host")
)

var (
	lastUpdate = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "packetframe_last_update",
		Help: "PacketFrame last update",
	})

	nodes = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "packetframe_node_status",
			Help: "PacketFrame Node Status",
		},
		[]string{"node", "geoloc"},
	)
)

func main() {
	flag.Parse()

	if *listenAddr == "" {
		flag.Usage()
		os.Exit(1)
	}

	log.Println("connecting to database")
	client, err := mongo.NewClient(options.Client().ApplyURI(*mongoAddr))
	if err != nil {
		log.Fatal(err)
	}
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}
	defer client.Disconnect(ctx)

	nodesCollection := client.Database("cdn").Collection("nodes")

	go func() {
		for {
			cursor, err := nodesCollection.Find(context.TODO(), bson.D{})
			if err != nil {
				log.Fatal(err)
			}

			for cursor.Next(context.TODO()) {
				var node map[string]interface{}
				err := cursor.Decode(&node)
				if err != nil {
					log.Fatal(err)
				}

				// ping node management IP
				log.Infof("pinging %s\n", node["management_ip"].(string))
				pinger, err := ping.NewPinger(node["management_ip"].(string))
				if err != nil {
					log.Warnln(err)
				}
				pinger.Count = 1
				pinger.SetPrivileged(true)

				err = pinger.Run()
				if err != nil {
					log.Warnf("ping run: %v\n", err)
				}

				statusCode := 0 // 0 for failure
				pinger.OnFinish = func(stats *ping.Statistics) {
					log.Printf("%s done\n", node["name"])
					if stats.PacketsSent == stats.PacketsRecv {
						log.Printf("%s working\n", node["name"])
						statusCode = 1
					}
				}

				// set labels and status code
				nodes.With(
					prometheus.Labels{
						"node":   node["name"].(string),
						"geoloc": node["geoloc"].(string),
					},
				).Add(float64(statusCode))
			}

			if err := cursor.Err(); err != nil {
				log.Warnln(err)
			}

			// close cursor connection
			cursor.Close(context.TODO())

			// set last updated time
			lastUpdate.SetToCurrentTime()
			time.Sleep(updateDelay)
		}
	}()

	http.Handle("/metrics", promhttp.Handler())
	log.Infof("Starting exporter: http://%s/metrics", *listenAddr)
	log.Fatal(http.ListenAndServe(*listenAddr, nil))
}
