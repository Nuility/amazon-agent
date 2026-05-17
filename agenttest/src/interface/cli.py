"""Command line interface for the demo application."""
import argparse
import json
import sys
from typing import Optional

from infrastructure.logger import Logger
from services.analysis_service import AnalysisService
from services.batch_service import BatchService
from services.config_service import ConfigService
from services.user_service import UserService


class CLI:
    def __init__(
        self,
        user_service: UserService,
        batch_service: BatchService,
        analysis_service: AnalysisService,
        config_service: ConfigService,
        logger: Logger,
    ):
        self.user_service = user_service
        self.batch_service = batch_service
        self.analysis_service = analysis_service
        self.config_service = config_service
        self.logger = logger

    def run(self, args: Optional[list] = None):
        parser = self._create_parser()
        parsed_args = parser.parse_args(args)
        if not getattr(parsed_args, "command", None):
            parser.print_help()
            return

        command_handler = getattr(self, f"_handle_{parsed_args.command}", None)
        if not command_handler:
            print(f"Unknown command: {parsed_args.command}")
            sys.exit(1)

        try:
            command_handler(parsed_args)
        except Exception as e:
            self.logger.error(f"CLI command failed: {str(e)}")
            print(f"Error: {str(e)}")
            sys.exit(1)

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="agenttest", description="User and ad-agent demo CLI")
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        create_parser = subparsers.add_parser("create", help="Create a user")
        create_parser.add_argument("--username", required=True)
        create_parser.add_argument("--email", required=True)
        create_parser.add_argument("--phone")
        create_parser.add_argument("--status", default="active")
        create_parser.add_argument("--tags")
        create_parser.add_argument("--attributes")
        create_parser.add_argument("--operator", default="cli")

        get_parser = subparsers.add_parser("get", help="Get one user")
        get_parser.add_argument("user_id")

        update_parser = subparsers.add_parser("update", help="Update a user")
        update_parser.add_argument("user_id")
        update_parser.add_argument("--username")
        update_parser.add_argument("--email")
        update_parser.add_argument("--phone")
        update_parser.add_argument("--status")
        update_parser.add_argument("--tags")
        update_parser.add_argument("--attributes")
        update_parser.add_argument("--operator", default="cli")

        delete_parser = subparsers.add_parser("delete", help="Delete a user")
        delete_parser.add_argument("user_id")
        delete_parser.add_argument("--physical", action="store_true")
        delete_parser.add_argument("--operator", default="cli")

        list_parser = subparsers.add_parser("list", help="List users")
        list_parser.add_argument("--status")
        list_parser.add_argument("--tag")
        list_parser.add_argument("--page", type=int, default=1)
        list_parser.add_argument("--page-size", type=int, default=20)

        batch_create_parser = subparsers.add_parser("batch-create", help="Batch create users from file")
        batch_create_parser.add_argument("--file", required=True)
        batch_create_parser.add_argument("--format", default="json")
        batch_create_parser.add_argument("--operator", default="cli")

        stats_parser = subparsers.add_parser("stats", help="Show statistics")
        stats_parser.add_argument("--status")

        analyze_parser = subparsers.add_parser("analyze", help="Run analysis")
        analyze_parser.add_argument("--type", choices=["anomalies", "suggestions"], default="anomalies")

        config_parser = subparsers.add_parser("config", help="Config management")
        config_parser.add_argument("--reload", action="store_true")
        config_parser.add_argument("--show", action="store_true")
        return parser

    def _handle_create(self, args):
        user_data = {"username": args.username, "email": args.email, "status": args.status}
        if args.phone:
            user_data["phone"] = args.phone
        if args.tags:
            user_data["tags"] = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
        if args.attributes:
            user_data["attributes"] = json.loads(args.attributes)

        result = self.user_service.create_user(user_data, args.operator)
        if result.success:
            user = result.data
            print(f"User created: {user.user_id} {user.username} {user.email}")
            return
        print(f"Create failed: {result.error_message}")

    def _handle_get(self, args):
        result = self.user_service.get_user(args.user_id)
        if result.success:
            print(json.dumps(result.data.to_dict(), ensure_ascii=False, indent=2))
            return
        print(f"Get failed: {result.error_message}")

    def _handle_update(self, args):
        update_data = {}
        for field in ("username", "email", "phone", "status"):
            value = getattr(args, field)
            if value:
                update_data[field] = value
        if args.tags:
            update_data["tags"] = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
        if args.attributes:
            update_data["attributes"] = json.loads(args.attributes)

        result = self.user_service.update_user(args.user_id, update_data, args.operator)
        if result.success:
            print(json.dumps(result.data.to_dict(), ensure_ascii=False, indent=2))
            return
        print(f"Update failed: {result.error_message}")

    def _handle_delete(self, args):
        result = self.user_service.delete_user(args.user_id, logical=not args.physical, operator=args.operator)
        print("Delete succeeded" if result.success else f"Delete failed: {result.error_message}")

    def _handle_list(self, args):
        filters = {}
        if args.status:
            filters["status"] = args.status
        if args.tag:
            filters["tags"] = [args.tag]
        result = self.user_service.list_users(filters or None, args.page, args.page_size)
        if result.success:
            print(json.dumps(result.data, ensure_ascii=False, indent=2))
            return
        print(f"List failed: {result.error_message}")

    def _handle_batch_create(self, args):
        result = self.batch_service.import_from_file(args.file, args.format, args.operator)
        if result.success:
            print(json.dumps(result.data.__dict__, ensure_ascii=False, indent=2))
            return
        print(f"Batch create failed: {result.error_message}")

    def _handle_stats(self, args):
        filters = {"status": args.status} if args.status else None
        result = self.analysis_service.get_statistics(filters)
        if result.success:
            print(json.dumps(result.data.to_dict(), ensure_ascii=False, indent=2))
            return
        print(f"Stats failed: {result.error_message}")

    def _handle_analyze(self, args):
        result = (
            self.analysis_service.detect_anomalies()
            if args.type == "anomalies"
            else self.analysis_service.get_operation_suggestions({})
        )
        if result.success:
            print(json.dumps(result.data, ensure_ascii=False, indent=2))
            return
        print(f"Analyze failed: {result.error_message}")

    def _handle_config(self, args):
        if args.reload:
            result = self.config_service.reload_config()
            print("Config reloaded" if result.success else f"Reload failed: {result.error_message}")
            return
        if args.show:
            print(json.dumps(self.config_service.get_config().to_dict(), ensure_ascii=False, indent=2))
            return
        print("No config action specified")
